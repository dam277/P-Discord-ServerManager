import nextcord

from ..Create import Create
from ...._commands.Command import Command

from .....database.models.tables.NoteList import NoteList
from .....database.models.tables.Note import Note
from .....database.models.tables.Server import Server

from .....utils.logger.Logger import Logger, LogDefinitions

class CreateNoteList(Create):
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
            CreateNoteList.__init__()
        
        Parameters :
        ---
            - name : :class:`str` => Name of the note list
            
        Returns :
        ---
            :class:`None`
        """
        self.name = name
        self.guild_id = guild_id

        super().__init__()

    @Command.register(name="note_list", description="Create a note list", parent="/create", note_list_name="Name of the note list")
    async def execute(self, interaction: nextcord.Interaction):
        """ # CreateNoteList command execute method
        
        Description :
        ---
            Execute the CreateNoteList command
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.CreateNoteList.py\n
            CreateNoteList.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Discord interaction
            
        Returns :
        ---
            :class:`None`
        """
        # Execute the parent function
        await super().execute(interaction)
        if not self.has_permission:
            return
        
        # Get the server id
        server_id_result = await Server.get_server_id_by_guild_id(self.guild_id)

        # Check if the server exists
        if not server_id_result.get("value") or not server_id_result.get("passed"):
            return await interaction.send(f"This server is not registered in the database, use /setup first", ephemeral=True) if server_id_result.get("error") is None else await interaction.send(f"An error occured while getting the server id : {server_id_result.get("error")}", ephemeral=True)
        
        # Check if the note list already exists
        note_list_result = await NoteList.get_note_list_by_name_and_fk_server(self.name, server_id_result.get("value"))
        if note_list_result.get("object") is not None:
            return await interaction.send(f"This note list already exists", ephemeral=True)
        
        # Create the note list
        result = await NoteList.create_note_list(self.name, server_id_result.get("value"))

        # Check if the query passed
        if not result.get("passed"):
            Logger.log(LogDefinitions.ERROR, f"An error occured while creating the note list : {result.get("error")}")
            return await interaction.send(f"An error occured while creating the note list : {result.get("error")}", ephemeral=True)
        
        # Send the message
        await interaction.send(f"Note list **{self.name}** created !")

