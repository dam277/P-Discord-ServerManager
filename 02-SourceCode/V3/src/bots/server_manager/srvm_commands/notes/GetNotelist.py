import nextcord

from ...._commands.Command import Command
from ..Get import Get

from .....database.models.tables.NoteList import NoteList
from .....database.models.tables.Server import Server
from .....database.models.tables.Note import Note
from .....database.models.tables.File import File

from ....server_manager.srvm_views.PageView import PageView

from .....utils.logger.Logger import Logger, LogDefinitions

class GetNoteList(Get):
    """ # GetNoteList command class
    
    Description :
    ---
        Manage the GetNoteList command discord command
    
    Access :
    ---
        src.bots.server_manager.srvm_commands.notes.GetNoteList.py\n
        GetNoteList
    
    inheritance :
    ---
        - Command : :class:`Command` => Parent class of database commands
    """
    def __init__(self, note_list_name: str, guild_id: int):
        """ # GetNoteList command constructor

        Description :
        ---
            Construct a GetNoteList command object
        
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.GetNoteList.py\n
            GetNoteList.__init__()
        
        Parameters :
        ---
            - note_list_name : :class:`str` => Name of the note list
            - guild_id : :class:`int` => Guild id of the note list
        
        Returns :
        ---
            :class:`None`
        """
        self.note_list_name = note_list_name
        self.guild_id = guild_id

        super().__init__()

    @Command.register(name="get_note_list", description="Get a note list from the discord server", parent="/get", note_list_name="Name of the note list")
    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute command function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the command and make all connections with models and frontend (discord chat)
        
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.GetNoteList.py\n
            GetNoteList.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Discord interaction object
        
        Returns :
        ---
            :class:`None`
        """

               # Execute the parent function
        # Execute the parent command
        await super().execute(interaction)
        if not self.has_permission:
            return
        
        # Get the server id
        server_id_result = await Server.get_server_id_by_guild_id(self.guild_id)

        # Check if the server exists
        if not server_id_result.get("value") or not server_id_result.get("passed"):
            return await interaction.send(f"This server is not registered in the database, use /setup first", ephemeral=True) if server_id_result.get("error") is None else await interaction.send(f"An error occured while getting the server id : {server_id_result.get("error")}", ephemeral=True)
        
        # Get the note list
        note_list_result = await NoteList.get_note_list_by_name_and_fk_server(self.note_list_name, server_id_result.get("value"))
        note_list = note_list_result.get("object")

        # Check if the note list exists
        if not note_list or not note_list_result.get("passed"):
            return await interaction.send(f"This note list doesn't exist", ephemeral=True) if note_list_result.get("error") is None else await interaction.send(f"An error occured while getting the note list : {note_list_result.get("error")}", ephemeral=True)
        
        # Get the associated notes
        notes_result = await Note.get_notes_by_note_list_id(note_list.id)
        notes = notes_result.get("objects")

        # Check if the notes exists
        if not notes or not notes_result.get("passed"):
            return await interaction.send(f"This note list **{note_list.name}** doesn't have any notes", ephemeral=True) if notes_result.get("error") is None else await interaction.send(f"An error occured while getting the notes : {notes_result.get("error")}", ephemeral=True)
        
        pages = []
        # Create a list of list of dictionaries with notes
        for i in range(0, len(notes), 5):
            pages.append([{"title": note.title, "text": note.text} for note in notes[i:i + 5]])

        # Make the notelist as embed
        note_list_embed = nextcord.Embed(title=note_list.name)

        # Page view for the embed
        page_view = PageView(pages, note_list_embed)
        await page_view.execute(interaction)

        # Check if the note list has an image
        if note_list.fk_file:
            # Get the file
            file_result = await File.get_file_by_id(note_list.fk_file)

            # Check if the file exists
            if file_result.get("object"):
                file = nextcord.File(file_result.get("object").path, filename='thumbnail.png')  
                note_list_embed.set_thumbnail(url='attachment://thumbnail.png')

            # Send the embed with the image
            return await interaction.send(file=file, embed=note_list_embed, view=page_view)

        # Send the embed without the image
        return await interaction.send(embed=note_list_embed, view=page_view)