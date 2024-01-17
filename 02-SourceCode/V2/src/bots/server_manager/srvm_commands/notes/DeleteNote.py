import nextcord

from ...._commands.Command import Command

from .....database.models.tables.Note import Note
from .....database.models.tables.Server import Server

from ...srvm_views.ConfirmationView import ConfirmationView

from .....utils.logger.Logger import Logger, LogDefinitions

class DeleteNote(Command):
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
        Logger.log(LogDefinitions.INFO, f"{__class__.__name__} command called by {interaction.user.name}")
        
        # Create a confirmation view
        confirmation_view = ConfirmationView()
        await interaction.send("Are you sure you want to delete this note ?", view=confirmation_view)
        await confirmation_view.wait()

        # If the user didn't confirm the deletion
        if not confirmation_view.value:
            await interaction.followup.send("Note deletion canceled")
            return
        
        # Get server id and note to delete it
        server_id = await Server.get_server_id_by_guild_id(self.guild_id)
        note = await Note.get_note_in_notelists_by_server_id_and_note_title(server_id, self.title)

        # Check if the note exists
        if not await self.check_object_type(note, Note, self.title, interaction):
            return
        
        # Delete the note and send a message
        message = await Note.delete_note_by_id(note.id)
        await interaction.followup.send(message)
        



