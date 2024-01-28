import nextcord

from ..Add import Add
from ...._commands.Command import Command

from .....database.models.tables.NoteList import NoteList
from .....database.models.tables.Note import Note
from .....database.models.tables.Server import Server

from .....utils.logger.Logger import Logger, LogDefinitions

class AddNote(Add):
    """ # AddNote command class
    
    Description :
    ---
        Manage the AddNote command discord command
    
    Access :
    ---
        src.bots.server_manager.srvm_commands.notes.AddNote.py\n
        AddNote
    
    inheritance :
    ---
        - Command : :class:`Command` => Parent class of database commands
    """
    def __init__(self, title: str, text: str, note_list_name: str, guild_id: int):
        """ # AddNote command constructor
        
        Description :
        ---
            Construct a AddNote command object
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.AddNote.py\n
            AddNote.__init__()
        
        Parameters :
        ---
            - title : :class:`str` => Title of the note
            - text : :class:`str` => Text of the note
            - note_list_name : :class:`str` => Name of the note list
            
        Returns :
        ---
            :class:`None`
        """
        self.title = title
        self.text = text
        self.note_list_name = note_list_name
        self.guild_id = guild_id

        super().__init__()

    @Command.register(name="note", description="Add a note into a note list", parent="/add", title="Title of the note", text="Text of the note", note_list_name="Name of the note list")
    async def execute(self, interaction: nextcord.Interaction):
        """ # AddNote command execute method
        
        Description :
        ---
            Execute the AddNote command
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.AddNote.py\n
            AddNote.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Discord interaction with the command
            
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
        
        # Get the note list id
        note_list_id_result = await NoteList.get_note_list_id_by_name_and_fk_server(self.note_list_name, server_id_result.get("value"))
        
        # Add the note list if it does not exists
        if not note_list_id_result.get("value") or not note_list_id_result.get("passed"):
            return await interaction.send(f"The note list **{self.note_list_name}** does not exists, use **/create note_list** to add it", ephemeral=True) if note_list_id_result.get("error") is None else await interaction.send(f"An error occured while getting the note list id : {note_list_id_result.get("error")}", ephemeral=True)
        
        # Check if the note already exists on this notelist
        notes_result = await Note.get_notes_by_note_list_id(note_list_id_result.get("value"))

        if (self.title == note.title for note in notes_result.get("objects")):
            return await interaction.send(f"The note {self.title} already exists in the note list {self.note_list_name}", ephemeral=True)
        
        # Add the note to the database
        result = await Note.add_note(self.title, self.text, note_list_id_result.get("value"))

        # Check if the note has been added
        if not result.get("passed"):
            return await interaction.send(f"An error occured while adding the note : {result.get("error")}", ephemeral=True)
        return await interaction.send(f"The note {self.title} has been added to the note list {self.note_list_name}", ephemeral=True)