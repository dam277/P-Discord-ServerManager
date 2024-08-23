import nextcord

from ...._commands.Command import Command
from ..Modify import Modify

from .....database.models.srvm_tables.Note import Note
from .....database.models.srvm_tables.Server import Server

from .....utils.logger.Logger import Logger, LogDefinitions

class ModifyNote(Modify):
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
    def __init__(self, title: str, new_title: str|None, new_text: str|None, guild_id: int):
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
        self.new_title = new_title
        self.new_text = new_text
        self.guild_id = guild_id

        super().__init__()

    @Command.register(name="modify_note", description="Modify a note from the server", parent="/modify", title="Title of the note to modify", new_title="[optional]New title of the note", new_text="[optional]New text of the note")
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
        # Execute the parent command
        await super().execute(interaction)
        if not self.has_permission:
            return
        
        # Get the server id
        server_id_result = await Server.get_server_id_by_guild_id(self.guild_id)

        # Check if the server exists
        if not server_id_result.get("value"):
            return await interaction.send("Server not found", ephemeral=True)
        
        # Get the note
        note_result = await Note.get_note_in_notelists_by_server_id_and_note_title(server_id_result.get("value"), self.title)

        # Check if the note exists
        if note_result.get("object") is None:
            return await interaction.send("Note doesn't exist", ephemeral=True)
        
        # Get the note object
        note = note_result.get("object")

        # Check if the user did send something
        if self.new_title is None and self.new_text is None:
            return await interaction.send("You must at least send a new title or new text to modify it", ephemeral=True)

        new_text = self.new_text if self.new_text else note.text
        new_title = self.new_title if self.new_title else note.title

        # Update the note
        update_note_result = await Note.update_note(note.id, new_title, new_text)

        # Check if the note has been updated
        if not update_note_result.get("passed"):
            return await interaction.send(f"Error while updating the note : {update_note_result.get("error")}", ephemeral=True)
        
        # Send the message
        await interaction.send(f"Note updated : {note.title}, {note.text} -> {new_title}, {new_text}", ephemeral=True)
        
