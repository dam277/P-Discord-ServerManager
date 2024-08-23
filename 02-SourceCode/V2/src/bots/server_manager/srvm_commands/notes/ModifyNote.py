import nextcord

from ...._commands.Command import Command

from .....database.models.tables.Note import Note
from .....database.models.tables.Server import Server

from .....utils.logger.Logger import Logger, LogDefinitions

class ModifyNote(Command):
    """ # ModifyNote command class
    
    Description :
    ---
        Manage the ModifyNote command discord command
    
    Access :
    ---
        src.bots.server_manager.srvm_commands.notes.ModifyNote.py\n
        ModifyNote
        
    inheritance :
    ---
        - Command : :class:`Command` => Parent class of database commands
    """
    def __init__(self, title: str, new_text: str, guild_id: int):
        """ # ModifyNote command constructor
        
        Description :
        ---
            Construct a ModifyNote command object
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.ModifyNote.py\n
            ModifyNote.__init__()
        
        Parameters :
        ---
            - title : :class:`str` => New title of the note
            - new_text : :class:`str` => New new_text of the note
            - guild_id : :class:`int` => Guild id of the note list
            
        Returns :
        ---
            :class:`None`
        """
        
        self.title = title
        self.new_text = new_text
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
            src.bots.server_manager.srvm_commands.notes.ModifyNote.py\n
            ModifyNote.execute()
            
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Discord interaction
            
        Returns :
        ---
            :class:`None`
        """
        Logger.log(LogDefinitions.INFO, f"{__class__.__name__} command called by {interaction.user.name}")

        # Get the server id and the note object
        server_id = await Server.get_server_id_by_guild_id(self.guild_id)
        note = await Note.get_note_in_notelists_by_server_id_and_note_title(server_id, self.title)

        # Check if the note exists
        if not await self.check_object_type(note, Note, self.title, interaction):
            return
        
        # Update the note
        message = await Note.update_note(note.id, self.new_text)
        
        # Send a message
        await interaction.send(content=message)