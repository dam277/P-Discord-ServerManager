import nextcord
from nextcord.ext import commands

from colorama import Fore

from .._commands.Command import Command

from ..Bot import Bot
from ...utils.logger.Logger import Logger, LogDefinitions
from ...utils.enums.Commands import Commands
from ...utils.enums.Events import Events
from ...utils.enums.Autocompletes import Autocompletes

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
    def __init__(self, discord_token: str, db_name: str):
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
        super().__init__(command_prefix, intents, discord_token, db_name)

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
            Logger.log(LogDefinitions.DEBUG, f"Channel {channel.name} has been deleted")
            
            event = Events.on_guild_channel_delete.value(channel)
            await event.execute()

        @self.bot_instance.event
        async def on_voice_state_update(member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState):
            """ # Bot on_voice_state_update event
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Event called when a user join or leave a voice channel\n
                This use :class:`ChannelEvents` class to execute this event

            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.events(on_voice_state_update())

            Parameters :
            ---
                - member : :class:`nextcord.Member` => Member who join or leave a voice channel
                - before : :class:`nextcord.VoiceState` => Voice state before the update
                - after : :class:`nextcord.VoiceState` => Voice state after the update

            Returns :
            ---
                :class:`None`
            """
            # Check if the user has joined or left a voice channel
            event = Events.on_voice_state_update.value(member, before, after)
            await event.execute()

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

        #region ==== Support commands ============================
        #region ---- Setup command ------------------------
        @self.bot_instance.slash_command(name="setup", description="Setup the server into the database to be able to use the bot with this discord server")
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
            command = Commands.setup.value(interaction.guild_id, interaction.guild.name)
            await command.execute(interaction)
        #endregion ---- Setup command ------------------------
            
        #region ---- help command ------------------------
        @self.bot_instance.slash_command(name="help", description="Get the list of usable commands")
        async def help(interaction: nextcord.Interaction):
            """ # Bot help command
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Get the list of commands\n
                This use :class:`GetCommands` class to execute this command

            Access : 
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(help())
            
            Parameters : 
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user

            Returns : 
            ---
                :class:`None`
            """
            command = Commands.help.value()
            await command.execute(interaction)
        #endregion ---- help command ------------------------
        #endregion ==== Support commands ============================    
        
        #region ==== Add commands ============================
        @self.bot_instance.slash_command(name="add", description="Add something to the server")
        async def add(interaction: nextcord.Interaction):
            """ # Bot add command
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Add something to the server\n
                This use :class:`Add` class to execute this command

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

        #region ---- Add file command ------------------------
        @add.subcommand(name="file", description="Add a file to the server")
        async def add_file(interaction: nextcord.Interaction, file: nextcord.Attachment):
            """ # Bot add file command
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Add a file to the server\n
                This use :class:`AddFile` class to execute this command

            Access : 
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(add_file())
            
            Parameters : 
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user

            Returns : 
            ---
                :class:`None`
            """
            command = Commands.add_file.value(interaction.guild_id, file)
            await command.execute(interaction)
        #endregion ---- Add file command ------------------------
            
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
            command = Commands.add_note.value(title, text, note_list_name, interaction.guild.id)
            await command.execute(interaction)
        #endregion ----------------------------
        #endregion ==== Add commands ============================
            
        #region ==== Create commands ============================
        @self.bot_instance.slash_command(name="create", description="Create something for the server")
        async def create(interaction: nextcord.Interaction):
            """ # Bot create command
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Create something for the server\n
                This use :class:`Create` class to execute this command

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

        #region ---- Create note list command ------------------------
        @create.subcommand(name="note_list", description="Create a note list")
        async def create_note_list(interaction: nextcord.Interaction, name:str, file_name: str|None):
            """ # Bot create note list command
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Create a note list\n
                This use :class:`CreateNoteList` class to execute this command
                
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(create_note_list())
            
            Parameters :
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
                """
            command = Commands.create_note_list.value(name, interaction.guild_id, file_name)
            await command.execute(interaction)
        #endregion ---- Create note list command ------------------------
            
        #region ---- Create private channel command ------------------------
        @create.subcommand(name="private_channel", description="Create a private channel to make user create their on category")
        async def create_private_channel(interaction: nextcord.Interaction, channel_name: str):
            """ # Bot create private channel command
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Create a private channel into the discord server which will make the users able to join it and automatically create a new private category for him\n
                This use :class:`CreatePrivateChannel` class to execute this command
                
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(private_channel())
            
            Parameters :
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
                """
            command = Commands.create_private_channel.value(interaction.guild_id, channel_name)
            await command.execute(interaction)
        #endregion ---- Create private channel command ------------------------
        #endregion ==== Create commands ============================

        #region ==== Get commands ============================
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

        #region ---- Get file command ------------------------
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
            command = Commands.get_file.value(file_name, interaction.guild.id)
            await command.execute(interaction)
        #endregion ---- Get file command ------------------------
        #region ---- Get note list command ------------------------
        @get.subcommand(name="notelist", description="Get a notelist")
        async def get_notelist(interaction: nextcord.Interaction, note_list_name: str):
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
            command = Commands.get_note_list.value(note_list_name, interaction.guild.id)
            await command.execute(interaction)
        #endregion ---- Get note list command ------------------------
        #endregion ==== Get commands ============================

        #region ==== Modify commands ============================
        @self.bot_instance.slash_command(name="modify", description="Modify something from the server")
        async def modify(interaction: nextcord.Interaction):
            """ # Bot modify command
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
        # region ---- Modify note command ------------------------
        @modify.subcommand(name="note", description="Modify a note from a notelist")
        async def modify_note(interaction: nextcord.Interaction, note_title: str, new_title: str = None, new_text: str = None):
            """ Bot modify note subcommand
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Modify a note to the server\n
                This command is a subcommand of the modify command
                
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(modify_note())
                
            Parameters :
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
                - title : :class:`str` => Title of the note to modify
                - new_text : :class:`str` => New text of the note
            
            Returns :
            ---
                :class:`None`
            """
            command = Commands.modify_note.value(note_title, new_title, new_text, interaction.guild.id)
            await command.execute(interaction)
        # endregion ---- Modify note command ------------------------
        #endregion ==== Modify commands ============================
            
        #region ==== Delete commands ============================
        @self.bot_instance.slash_command(name="delete", description="Delete something from the server")
        async def delete(interaction: nextcord.Interaction):
            """ # Bot delete command
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
        #region ---- Delete file command ------------------------
        @delete.subcommand(name="file", description="Delete a file from the server")
        async def delete_file(interaction: nextcord.Interaction, file_name: str):
            """ Bot delete file subcommand
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Delete a file to the server\n
                This command is a subcommand of the delete command
                
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(delete_file())
                
            Parameters :
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
                - file_name : :class:`str` => Name of the file to delete
            
            Returns :
            ---
                :class:`None`
            """
            command = Commands.delete_file.value(file_name, interaction.guild.id)
            await command.execute(interaction)
        #endregion ---- Delete file command ------------------------
        #region ---- Delete note command ------------------------
        @delete.subcommand(name="note", description="Delete a note from a notelist")
        async def delete_note(interaction: nextcord.Interaction, note_title: str):
            """ Bot delete note subcommand
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Delete a note to the server\n
                This command is a subcommand of the delete command
                
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(delete_note())
                
            Parameters :
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
                - note_title : :class:`str` => Title of the note to delete
                - note_list_name : :class:`str` => Name of the notelist where the note is
            
            Returns :
            ---
                :class:`None`
            """
            command = Commands.delete_note.value(note_title, interaction.guild.id)
            await command.execute(interaction)
        #endregion ---- Delete note command ------------------------
        #region ---- Delete note list command ------------------------
        @delete.subcommand(name="notelist", description="Delete a notelist")
        async def delete_notelist(interaction: nextcord.Interaction, note_list_name: str):
            """ Bot delete notelist subcommand
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Delete a notelist to the server\n
                This command is a subcommand of the delete command
                
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(delete_notelist())
                
            Parameters :
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
                - name : :class:`str` => Name of the notelist to delete
            
            Returns :
            ---
                :class:`None`
            """
            command = Commands.delete_note_list.value(note_list_name, interaction.guild.id)
            await command.execute(interaction)
        #endregion ---- Delete note list command ------------------------
        #endregion ==== Delete commands ============================

        #region ==== Autocompletes ============================
        @get_file.on_autocomplete("file_name")
        @create_note_list.on_autocomplete("file_name")
        @delete_file.on_autocomplete("file_name")
        async def file_autocomplete(interaction: nextcord.Interaction, current: str):
            """ # Bot file autocomplete
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Get a file from the server\n
                This use :class:`FileAutocomplete` class to execute this autocomplete
                
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(file_autocomplete())
            
            Parameters :
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
                """
            autocomplete = Autocompletes.file_autocomplete.value(current, interaction.guild_id)
            await autocomplete.execute(interaction)

        @add_note.on_autocomplete("note_list_name")
        @get_notelist.on_autocomplete("note_list_name")
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
            autocomplete = Autocompletes.notelist_autocomplete.value(current, interaction.guild.id)
            await autocomplete.execute(interaction)
        
        @delete_note.on_autocomplete("note_title")
        @modify_note.on_autocomplete("note_title")
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
            autocomplete = Autocompletes.note_autocomplete.value(current, interaction.guild.id)
            await autocomplete.execute(interaction)
        #endregion ==== Autocompletes ============================
#region temp imports
# from .srvm_commands.setup.Setup import Setup
# from .srvm_commands.help.GetCommands import GetCommands
# from .srvm_commands.files.AddFile import AddFile
# from .srvm_commands.files.DeleteFile import DeleteFile 
# from .srvm_commands.files.GetFile import GetFile 
# from .srvm_commands.notes.CreateNoteList import CreateNoteList 
# from .srvm_commands.notes.GetNoteList import GetNoteList 
# from .srvm_commands.notes.AddNote import AddNote 
# from .srvm_commands.notes.ModifyNote import ModifyNote
# from .srvm_commands.notes.DeleteNote import DeleteNote
# from .srvm_commands.notes.DeleteNoteList import DeleteNoteList
# from .srvm_commands.channels.CreatePrivateChannel import CreatePrivateChannel

# from .srvm_events.ChannelEvents import ChannelEvents

# from .srvm_autocompletes.files.FileAutocomplete import FileAutocomplete
# from .srvm_autocompletes.notes.NotelistAutocomplete import NotelistAutocomplete
# from .srvm_autocompletes.notes.NoteAutocomplete import NoteAutocomplete
#endregion temp imports