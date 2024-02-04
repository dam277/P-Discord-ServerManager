import nextcord

from ...._commands.Command import Command
from ..Delete import Delete

from .....database.models.tables.Note import Note
from .....database.models.tables.Server import Server

from ...srvm_views.ConfirmationView import ConfirmationView

from .....utils.logger.Logger import Logger, LogDefinitions

class DeleteNote(Delete):
    """ # DeleteNote command class
    
    Description :
    ---
        Manage the DeleteNote command discord command
    
    Access :
    ---
        src.bots.server_manager.srvm_commands.notes.DeleteNote.py\n
        DeleteNote
        
    inheritance :
    ---
        - Command : :class:`Command` => Parent class of database commands
    """
    def __init__(self, title: str, guild_id: int):
        """ # DeleteNote command constructor
        
        Description :
        ---
            Construct a DeleteNote command object
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.DeleteNote.py\n
            DeleteNote.__init__()
        
        Parameters :
        ---
            - title : :class:`str` => Title of the note
            - guild_id : :class:`int` => Guild id of the note list
            
        Returns :
        ---
            :class:`None`
        """
        
        self.title = title
        self.guild_id = guild_id

        super().__init__()

    @Command.register(name="delete_note", description="Delete a note from the server", parent="/delete", title="Title of the note to delete")
    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute command function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the command and make all connections with models and frontend (discord chat)       
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.DeleteNote.py\n
            DeleteNote.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Discord interaction object
            
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
        if not server_id_result.get("value"):
            return await interaction.send("Server not found", ephemeral=True)
        
        # Get the note
        note_result = await Note.get_note_in_notelists_by_server_id_and_note_title(server_id_result.get("value"), self.title)

        # Check if the note exists
        if note_result.get("object") is None:
            return await interaction.send("Note doesn't exist", ephemeral=True)
            
        # Get the note
        note = note_result.get("object")

        # Delete the note
        delete_result = await Note.delete_note_by_id(note.id)
        if not delete_result.get("passed"):
            return await interaction.send(f"Error while deleting the note, {delete_result.get("error")}", ephemeral=True)
        
        # Send the confirmation view
        confirmation_view = ConfirmationView()
        await confirmation_view.execute(interaction, "Are you sure you want to delete this note ?")

        # Check if the user confirmed
        if not confirmation_view.value:
            return await interaction.send("Note deletion canceled", ephemeral=True)
        
        # Send the confirmation message
        await interaction.followup.send(f"Note **{self.title}** deleted")

        



