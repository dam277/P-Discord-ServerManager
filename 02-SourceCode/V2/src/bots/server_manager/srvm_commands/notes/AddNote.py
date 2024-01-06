import nextcord

from ...._commands.Command import Command

from .....database.models.tables.NoteList import NoteList
from .....database.models.tables.Note import Note
from .....database.models.tables.Server import Server

from .....utils.logger.Logger import Logger, LogDefinitions

class AddNote(Command):
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

    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute command function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the command and make all connections with models and frontend (discord chat)
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.AddNote.py\n
            AddNote.execute()
            
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => interaction of the user with the bot
            
        Returns :
        ---
            :class:`None`
        """
        Logger.log(LogDefinitions.INFO, f"{__class__.__name__} command called by {interaction.user.name}")
        
        # Get the server
        id_server = await Server.get_server_id_by_guild_id(self.guild_id)

        # Get the note list
        note_list_id = await NoteList.get_note_list_id_by_name_and_fk_server(self.note_list_name, id_server)

        # Add the note to the notelist
        message = await Note.add_note(self.title, self.text, note_list_id)

        # Send the note to the user
        await interaction.response.send_message(content=message)