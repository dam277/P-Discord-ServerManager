import nextcord

from ...._commands.Command import Command
from ..Delete import Delete

from .....database.models.srvm_tables.Note import Note
from .....database.models.srvm_tables.NoteList import NoteList
from .....database.models.srvm_tables.Server import Server

from ...srvm_views.ConfirmationView import ConfirmationView

from .....utils.logger.Logger import Logger, LogDefinitions

class DeleteNoteList(Delete):
    """ # DeleteNoteList command class
    
    Description :
    ---
        Manage the DeleteNoteList command discord command
    
    Access :
    ---
        src.bots.server_manager.srvm_commands.notes.DeleteNoteList.py\n
        DeleteNoteList
        
    inheritance :
    ---
        - Command : :class:`Command` => Parent class of database commands
    """
    def __init__(self, note_list_name: str, guild_id: int):
        """ # DeleteNoteList command constructor
        
        Description :
        ---
            Construct a DeleteNoteList command object
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.DeleteNoteList.py\n
            DeleteNoteList.__init__()
        
        Parameters :
        ---
            - guild_id : :class:`int` => Guild id of the note list
            
        Returns :
        ---
            :class:`None`
        """
        
        self.note_list_name = note_list_name
        self.guild_id = guild_id

        super().__init__()
    
    @Command.register(name="delete_note_list", description="Delete a note list and all of its notes from the server", parent="/delete", note_list_name="Name of the note list to delete")
    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute command function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the command and make all connections with models and frontend (discord chat)
        
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.DeleteNoteList.py\n
            DeleteNoteList.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Discord interaction object
            
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
        if not server_id_result.get("value"):
            return await interaction.send("Server not found", ephemeral=True)
        
        # Get the note list id
        note_list_id_result = await NoteList.get_note_list_id_by_name_and_fk_server(self.note_list_name, server_id_result.get("value"))

        # Check if the note exists
        if not note_list_id_result.get("value"):
            return await interaction.send("Note doesn't exist", ephemeral=True)
        
        # Create a confirmation view
        confirmation_view = ConfirmationView()
        await confirmation_view.execute(interaction, "Are you sure you want to delete this note list ?")

        # If the user didn't confirm the deletion
        if not confirmation_view.value:
            return await interaction.followup.send("Note list deletion canceled")
        
        # Delete the notes
        notes_delete_result = await Note.delete_notes_by_id_notelist(note_list_id_result.get("value"))

        # Check if the notes were deleted
        if not notes_delete_result.get("passed"):
            return await interaction.send(f"Error while deleting the notes, {notes_delete_result.get("error")}", ephemeral=True)
        
        # Delete the note list
        note_list_delete_result = await NoteList.delete_note_list_by_id(note_list_id_result.get("value"))

        # Check if the note list was deleted
        if not note_list_delete_result.get("passed"):
            return await interaction.send(f"Error while deleting the note list, {note_list_delete_result.get("error")}", ephemeral=True)
        
        # Send the confirmation message
        await interaction.followup.send(f"Note list **{self.note_list_name}** deleted")            