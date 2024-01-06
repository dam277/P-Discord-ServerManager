import nextcord

from ...._commands.Command import Command

from .....database.models.tables.NoteList import NoteList
from .....database.models.tables.Server import Server
from .....database.models.tables.Note import Note

from ...._views.PageView import PageView

from .....utils.logger.Logger import Logger, LogDefinitions

class GetNoteList(Command):
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
        Logger.log(LogDefinitions.INFO, f"{__class__.__name__} command called by {interaction.user.name}")
        
        # Get the server
        id_server = await Server.get_server_id_by_guild_id(self.guild_id)

        # Get the note list
        note_list = await NoteList.get_note_list_by_name_and_fk_server(self.note_list_name, id_server)

        # Check if note list exists
        if not await self.check_object_type(note_list, NoteList, self.note_list_name, interaction):
            return
    
        # Make the notelist as embed
        note_list_embed = nextcord.Embed(title=note_list.name)

        # Get the associated notes
        notes = await Note.get_notes_by_note_list_id(note_list.id)

        # Check if the note list is empty
        if not notes:
            await interaction.send(f"This note list **{note_list.name}** is empty")
            return
        
        # Create a list of lists of pages with 5 notes
        notes_pages = [notes[i:i + 5] for i in range(0, len(notes), 5)]
        
        # Add the notes to the embed
        for note in notes_pages[0]:
            note_list_embed.add_field(name=note.title, value=note.text, inline=False)

        # Page view for the embed
        page_view = PageView(notes_pages)
        note_list_embed.set_footer(text=f"Page 1/{len(notes_pages)}")

        # Send the embed
        await interaction.send(embed=note_list_embed, view=page_view)
        page_view.wait()