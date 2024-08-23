import nextcord

from ...._commands.Command import Command

from .....database.models.tables.NoteList import NoteList
from .....database.models.tables.Server import Server

from .....utils.logger.Logger import Logger, LogDefinitions

class CreateNoteList(Command):
    """ # CreateNoteList command class 
    
    Description :
    ---
        Manage the CreateNoteList command discord command
    
    Access :
    ---
        src.bots.server_manager.srvm_commands.notes.CreateNoteList.py\n
        CreateNoteList
    
    inheritance :
    ---
        - Command : :class:`Command` => Parent class of database commands
    """
    def __init__(self, name: str, guild_id: int):
        """ # CreateNoteList command constructor

        Description :
        ---
            Construct a CreateNoteList command object
        
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.CreateNoteList.py\n
            CreateNoteList.__init_()
        
        Parameters :
        ---
            - name : :class:`str` => name of the command
        
        Returns :
        ---
            :class:`None`
        """
        self.name = name
        self.guild_id = guild_id

        super().__init__()

    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute command function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the command and make all connections with models and frontend (discord chat)
        
        Access :
        ---
            src.bots.server_manager.bot_commands.notes.CreateNoteList.py\n
            CreateNoteList.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => interaction of the user with the bot
        
        Returns :
        ---
            :class:`None`
        """
        Logger.log(LogDefinitions.INFO, f"{__class__.__name__} command called by {interaction.user.name}")

        # Get server id
        server_id = await Server.get_server_id_by_guild_id(self.guild_id)
        if server_id is None:
            await interaction.send("The server does not exists in database... Make a /setup first")
            Logger.log(LogDefinitions.WARNING, f"Server {self.guild_id} does not exists in database")
            return
        
        # Check if the note list already exists
        note_list = await NoteList.get_note_list_by_name_and_fk_server(self.name, server_id)
        if await self.check_object_type(note_list, NoteList, self.name, interaction, False):
            await interaction.send(f"This note list name **'{self.name}'** already exists")
            Logger.log(LogDefinitions.WARNING, f"Note list {self.name} already exists in server {self.guild_id}")
            return
        
        # Create the note list
        message = await NoteList.create_note_list(self.name, server_id)

        # Send the response
        await interaction.send(content=message)