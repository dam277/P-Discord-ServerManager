import nextcord

from ...._commands.Command import Command

from .....database.models.tables.Note import Note
from .....database.models.tables.NoteList import NoteList
from .....database.models.tables.Server import Server

from ...srvm_views.ConfirmationView import ConfirmationView

from .....utils.logger.Logger import Logger, LogDefinitions

class DeleteNoteList(Command):
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
    def __init__(self, name: str, guild_id: int):
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
            src.bots.server_manager.srvm_commands.notes.DeleteNoteList.py\n
            DeleteNoteList.execute()
        
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
        await interaction.send("Are you sure you want to delete this notelist and all the note associated with ?", view=confirmation_view)
        await confirmation_view.wait()

        # If the user didn't confirm the deletion
        if not confirmation_view.value:
            await interaction.followup.send("Note list deletion canceled")
            return
        
        # Get the server id
        server_id = await Server.get_server_id_by_guild_id(self.guild_id)

        # Get the note list id 
        note_list_id = await NoteList.get_note_list_id_by_name_and_fk_server(self.name, server_id)

        # Delete all the associated notes
        message = await Note.delete_notes_by_id_notelist(note_list_id)
        await interaction.followup.send(message)

        # Delete the note list and send a message
        message = await NoteList.delete_note_list_by_id(note_list_id)
        await interaction.followup.send(message)