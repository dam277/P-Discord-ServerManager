import nextcord
from colorama import Fore

from ..Bot import Bot

from .srvm_commands.setup.Setup import Setup
from .srvm_commands.help.GetCommands import GetCommands
from .srvm_commands.files.AddFile import AddFile
from .srvm_commands.files.DeleteFile import DeleteFile 
from .srvm_commands.files.GetFile import GetFile 
from .srvm_commands.notes.CreateNoteList import CreateNoteList 
from .srvm_commands.notes.GetNoteList import GetNoteList 
from .srvm_commands.notes.AddNote import AddNote 
from .srvm_commands.notes.ModifyNote import ModifyNote
from .srvm_commands.notes.DeleteNote import DeleteNote
from .srvm_commands.notes.DeleteNoteList import DeleteNoteList
from .srvm_commands.channels.CreatePrivateChannel import CreatePrivateChannel

from .srvm_events.ChannelEvents import ChannelEvents

from .srvm_autocompletes.files.FileAutocomplete import FileAutocomplete
from .srvm_autocompletes.notes.NotelistAutocomplete import NotelistAutocomplete
from .srvm_autocompletes.notes.NoteAutocomplete import NoteAutocomplete

from ...utils.logger.Logger import Logger, LogDefinitions

class ServerManagerBot(Bot):
    """ # Server manager bot class
        
    Description :
    ---
        Class of a bot that called "server manager bot"

    Access : 
    ---
        src.bots.server_manager.ServerManagerBot.py\n
        ServerManagerBot

    inheritance : 
    ---
        - Bot : :class:`Bot` => Parent class of bots
    """
    def __init__(self, discord_token: str):
        """ # Constructor of server manager bot
        
        Description :
        ---
            Construct an object of :class:`ServerManagerBot`

        Access : 
        ---
            src.bots.server_manager.ServerManagerBot.py\n
            ServerManagerBot.__init__

        Parameters : 
        ---
            - discord_token : :class:`str` => Token of the discord bot

        Returns : 
        ---
            :class:`None`
        """
        Logger.log(LogDefinitions.INFO, f"Constructing {__class__.__name__} object")
        command_prefix = "$"                                        # Set command prefix
        intents = nextcord.Intents.all()                            # Set the intents list

        # Set the datas into the parent
        super().__init__(command_prefix, intents, discord_token)

        # Setup bot interactions
        self.events()
        self.regular_commands()
        self.slash_commands()

    def events(self):
        """ # Events of the bot
        
        Description :
        ---
            Setup the events for the bot
        
        Access : 
        ---
            src.bots.server_manager.ServerManagerBot.py\n
            ServerManagerBot.events()
            
        Returns : 
        ---
            :class:`None`
        """
        Logger.log(LogDefinitions.INFO, f"Setting up {__class__.__name__} events")

        @self.bot_instance.event
        async def on_message(message: nextcord.Message):
            """ # Bot on_message event
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Event called when the bot receive a message\n
                This check if the message is a command or not and process it

            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.events(on_message())

            Parameters :
            ---
                - message : :class:`nextcord.Message` => Message received by the bot

            Returns :
            ---
                :class:`None`
            """
            # Check if the message is a command or not and process it
            if message.content.startswith(self.bot_instance.command_prefix):
                await self.bot_instance.process_commands(message)
            else:
                print(f"{Fore.WHITE} -> {message.author}: {message.content} {Fore.RESET}")
                
                # Check if the author is the bot himself
                if message.author == self.bot_instance.user:
                    return
        
        @self.bot_instance.event
        async def on_guild_channel_delete(channel: nextcord.abc.GuildChannel):
            """ # Bot on_guild_channel_delete event
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Event called when a channel is deleted\n
                This use :class:`ChannelEvents` class to execute this event

            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.events(on_guild_channel_delete())

            Parameters :
            ---
                - channel : :class:`nextcord.abc.GuildChannel` => Channel deleted

            Returns :
            ---
                :class:`None`
            """
            event = ChannelEvents(channel)
            await event.on_guild_channel_delete()


    def regular_commands(self):
        """ # Regular commands of the bot
        
        Description :
        ---
            Setup the regular commands for the bot
        
        Access : 
        ---
            src.bots.server_manager.ServerManagerBot.py\n
            ServerManagerBot.regular_commands()
            
        Returns : 
        ---
            :class:`None`
        """
        Logger.log(LogDefinitions.INFO, f"Setting up {__class__.__name__} regular commands")

    def slash_commands(self):
        """ # Slash commands of the bot
        
        Description :
        ---
            Setup the slash commands for the bot
        
        Access : 
        ---
            src.bots.server_manager.ServerManagerBot.py\n
            ServerManagerBot.slash_commands()
            
        Returns : 
        ---
            :class:`None`
        """
        Logger.log(LogDefinitions.INFO, f"Setting up {__class__.__name__} slash commands")
        
        #region ==== commands ======================================================================================================================
        #region ---- Setup command ------------------------
        @self.bot_instance.slash_command(name="setup", description="Setup the server into the database")
        async def setup(interaction: nextcord.Interaction):
            """ # Bot setup command
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Setup the actual discord server (guild) into the database\n
                This use :class:`Setup` class to execute this command

            Access : 
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(setup())
            
            Parameters : 
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user

            Returns : 
            ---
                :class:`None`
            """
            command = Setup(interaction.guild.id, interaction.guild.name)
            await command.execute(interaction)
        #endregion ---- Setup command ------------------------

        #region ---- Create commands ------------------------
        @self.bot_instance.slash_command(name="create", description="Create something (this is a parent command, you need to use a proposed subcommand)")
        async def create(interaction: nextcord.Interaction):
            """ # Bot create command
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Create something to the server\n
                This command is a parent command for the subcommands

            Access : 
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(create())

            Parameters : 
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user

            Returns : 
            ---
                :class:`None`
            """
            pass
        
        #region ---- subcommands ------------------------
        # ---- Create NoteList command ------------------------
        @create.subcommand(name="notelist", description="Create a notelist")
        async def create_notelist(interaction: nextcord.Interaction, name: str):
            """ # Bot create notelist subcommand
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Create a notelist to the server\n
                This command is a subcommand of the create command

            Access : 
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(create_notelist())

            Parameters : 
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
                - name : :class:`str` => Name of the notelist to create

            Returns : 
            ---
                :class:`None`
            """
            command = CreateNoteList(name, interaction.guild.id)
            await command.execute(interaction)

        # ---- Create Note command ------------------------
        @create.subcommand(name="privatechannel", description="Create a private channel")
        async def create_private_channel(interaction: nextcord.Interaction, name: str):
            """ # Bot create private channel subcommand
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Create a private channel to the server\n
                This command is a subcommand of the create command

            Access : 
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(create_private_channel())

            Parameters : 
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
                - name : :class:`str` => Name of the private channel to create

            Returns : 
            ---
                :class:`None`
            """
            command = CreatePrivateChannel(interaction.guild.id, name)
            await command.execute(interaction)
        #endregion ----------------------------
        #endregion ----------------------------

        #region ---- Get commands ------------------------
        @self.bot_instance.slash_command(name="get", description="Get something (this is a parent command, you need to use a proposed subcommand)")
        async def get(interaction: nextcord.Interaction):
            """ # Bot get command
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Get something from the server\n
                This command is a parent command for the subcommands
            
            Access : 
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(get())
            
            Parameters : 
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
            
            Returns : 
            ---
                :class:`None`
            """
            pass
        
        #region ---- subcommands ------------------------
        # ---- Get commands command ------------------------
        @get.subcommand(name="commands", description="Get all the usable commands of the bot")
        async def get_commands(interaction: nextcord.Interaction):
            """ # Bot get_commands command
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Get all the bot's functions and reply the user with an embed into the discord chat\n
                This use :class:`GetCommands` class to execute this command
            
            Access : 
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(get_commands())

            Parameters : 
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user

            Returns : 
            ---
                :class:`None`
            """
            command = GetCommands(slash_commands=self.bot_instance.get_all_application_commands(), regular_commands=self.bot_instance.commands)
            await command.execute(interaction)
        
        # ---- Get file command ------------------------
        @get.subcommand(name="file", description="Get a file from the server")
        async def get_file(interaction: nextcord.Interaction, file_name: str):
            """ Bot get file subcommand
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Get a file to the server\n
                This command is a subcommand of the get command
                
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(get_file())
                
            Parameters :
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
                - file : :class:`nextcord.Attachment` => File to get to the server
            
            Returns :
            ---
                :class:`None`
            """
            command = GetFile(file_name, interaction.guild.id)
            await command.execute(interaction)
        
        # ---- Get note list command ------------------------
        @get.subcommand(name="notelist", description="Get a notelist")
        async def get_notelist(interaction: nextcord.Interaction, name: str):
            """ Bot get notelist subcommand
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Get a notelist to the server\n
                This command is a subcommand of the get command
                
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(get_notelist())
                
            Parameters :
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
                - name : :class:`str` => Name of the notelist to get
            
            Returns :
            ---
                :class:`None`
            """
            command = GetNoteList(name, interaction.guild.id)
            await command.execute(interaction)
        #endregion ----------------------------
        #endregion ----------------------------
            
        #region ---- Add commands ------------------------
        @self.bot_instance.slash_command(name="add", description="Add something (this is a parent command, you need to use a proposed subcommand)")
        async def add(interaction: nextcord.Interaction):
            """" Bot add command
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Add something to the server\n
                This command is a parent command for the subcommands
                
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(add())
            
            Parameters :
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
            
            Returns :
            ---
                :class:`None` 
            """
            pass
        
        #region ---- subcommands ------------------------
        # ---- Add file command ------------------------
        @add.subcommand(name="file", description="Add a file to the server")
        async def add_file(interaction: nextcord.Interaction, file: nextcord.Attachment):
            """ Bot add file subcommand
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Add a file to the server\n
                This command is a subcommand of the add command
                
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(add_file())
                
            Parameters :
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
                - file : :class:`nextcord.Attachment` => File to add to the server
            
            Returns :
            ---
                :class:`None`
            """
            command = AddFile(interaction.guild.id, file)
            await command.execute(interaction)
        #endregion ----------------------------
            
        #region ---- Add note command ------------------------
        @add.subcommand(name="note", description="Add a note to a notelist")
        async def add_note(interaction: nextcord.Interaction, title: str, text: str, note_list_name: str):
            """ Bot add note subcommand
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Add a note to a notelist\n
                This command is a subcommand of the add command
                
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(add_note())
            
            Parameters :
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
            
            Returns :
            ---
                :class:`None`
            """
            command = AddNote(title, text, note_list_name, interaction.guild.id)
            await command.execute(interaction)
        #endregion ----------------------------
        #endregion ----------------------------

        #region ---- Modify commands ------------------------
        @self.bot_instance.slash_command(name="modify", description="Modify something (this is a parent command, you need to use a proposed subcommand)")
        async def modify(interaction: nextcord.Interaction):
            """ Bot modify command
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Modify something from the server\n
                This command is a parent command for the subcommands
                
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(modify())
            
            Parameters :
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
            
            Returns :
            ---
                :class:`None` 
            """
            pass

        #region ---- subcommands ------------------------
        # ---- Modify note command ------------------------
        @modify.subcommand(name="note", description="Modify a note")
        async def modify_note(interaction: nextcord.Interaction, title: str, new_text: str):
            """ Bot modify note subcommand
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Modify a note from the server\n
                This command is a subcommand of the modify command
                
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(modify_note())
                
            Parameters :
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
                - title : :class:`str` => New title of the note
                - new_text : :class:`str` => New text of the note
                
            Returns :
            ---
                :class:`None`
            """
            command = ModifyNote(title, new_text, interaction.guild.id)
            await command.execute(interaction)
        #endregion ----------------------------
        #endregion ----------------------------

        #region ---- Delete commands ------------------------
        @self.bot_instance.slash_command(name="delete", description="Delete something (this is a parent command, you need to use a proposed subcommand)")
        async def delete(interaction: nextcord.Interaction):
            """ Bot delete command
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Delete something from the server\n
                This command is a parent command for the subcommands
                
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(delete())
            
            Parameters :
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
            
            Returns :
            ---
                :class:`None` 
            """
            pass

        #region ---- subcommands ------------------------
        # ---- Delete file command ------------------------
        @delete.subcommand(name="file", description="Delete a file from the server")
        async def delete_file(interaction: nextcord.Interaction, file_name: str):
            """ Bot delete file subcommand
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Delete a file from the server\n
                This command is a subcommand of the delete command
            
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(delete_file())

            Parameters:
                interaction :class:`nextcord.Interaction`: The interaction object representing the user's interaction with the bot.
            
            Returns:
                :class:`None`
            """
            command = DeleteFile(file_name, interaction.guild.id)
            await command.execute(interaction)
        #endregion ----------------------------
            
        #region ---- Delete note command ------------------------
        @delete.subcommand(name="note", description="Delete a note from a notelist")
        async def delete_note(interaction: nextcord.Interaction, title: str):
            """ Bot delete note subcommand
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Delete a note from a notelist\n
                This command is a subcommand of the delete command
            
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(delete_note())

            Parameters:
                interaction :class:`nextcord.Interaction`: The interaction object representing the user's interaction with the bot.
                title :class:`str`: The title of the note to delete
            
            Returns:
                :class:`None`
            """
            command = DeleteNote(title, interaction.guild.id)
            await command.execute(interaction)
        #endregion ----------------------------
        #region ---- Delete notelist command ------------------------
        @delete.subcommand(name="notelist", description="Delete a notelist")
        async def delete_notelist(interaction: nextcord.Interaction, note_list_name: str):
            """ Bot delete notelist subcommand
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Delete a notelist\n
                This command is a subcommand of the delete command
            
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(delete_notelist())

            Parameters:
                interaction :class:`nextcord.Interaction`: The interaction object representing the user's interaction with the bot.
                name :class:`str`: The name of the notelist to delete
            
            Returns:
                :class:`None`
            """
            command = DeleteNoteList(note_list_name, interaction.guild.id)
            await command.execute(interaction)
        #endregion ----------------------------
        #endregion ----------------------------
        #endregion ==========================================================================================================================
            
        #region ==== autocompletes ======================================================================================================================
        # Create autocomplete function for file subcommands
        @get_file.on_autocomplete("file_name")
        @delete_file.on_autocomplete("file_name")
        async def file_autocomplete(interaction: nextcord.Interaction, current: str):
            """ Bot file autocomplete function
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Autocomplete function for the file subcommand
            
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands_file_autocomplete())

            Parameters:
                interaction :class:`nextcord.Interaction`: The interaction object representing the user's interaction with the bot.
            
            Returns:
                :class:`None`
            """
            autocomplete = FileAutocomplete(current, interaction.guild.id)
            return await autocomplete.execute(interaction)
        
        # Create autocomplete function for notes and notelists subcommands
        @get_notelist.on_autocomplete("name")
        @add_note.on_autocomplete("note_list_name")
        @delete_notelist.on_autocomplete("note_list_name")
        async def notelist_autocomplete(interaction: nextcord.Interaction, current: str):
            """ Bot note autocomplete function
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Autocomplete function for the notes and notelists subcommands
            
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands_note_autocomplete())

            Parameters:
                interaction :class:`nextcord.Interaction`: The interaction object representing the user's interaction with the bot.
            
            Returns:
                :class:`None`
            """
            autocomplete = NotelistAutocomplete(current, interaction.guild.id)
            return await autocomplete.execute(interaction)
        
        @modify_note.on_autocomplete("title")
        @delete_note.on_autocomplete("title")
        async def note_autocomplete(interaction: nextcord.Interaction, current: str):
            """ Bot note autocomplete function
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Autocomplete function for the note title subcommand
            
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands_note_title_autocomplete())

            Parameters:
                interaction :class:`nextcord.Interaction`: The interaction object representing the user's interaction with the bot.
            
            Returns:
                :class:`None`
            """
            autocomplete = NoteAutocomplete(current, interaction.guild.id)
            return await autocomplete.execute(interaction)
        #endregion ==========================================================================================================================