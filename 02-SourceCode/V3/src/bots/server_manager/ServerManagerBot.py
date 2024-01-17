import nextcord
from nextcord.ext import commands

from colorama import Fore

from .._commands.Command import Command

from ..Bot import Bot
from ...utils.logger.Logger import Logger, LogDefinitions
from ...utils.enums.Commands import Commands

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

        async def execute(interaction: nextcord.Interaction, command: Command):
            """ # Execute an element that inherit from :class:`Base`
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Execute a command

            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(execute_command())

            Parameters :
            ---
                - interaction : :class:`nextcord.Interaction` => Interaction with the user
                - command : :class:`Command` => Command to execute

            Returns :
            ---
                :class:`None`
            """
            await command.execute(interaction=interaction)        

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
            command = Commands.setup.value(interaction.guild_id, interaction.guild.name)
            await execute(interaction=interaction, command=command)
        #endregion ---- Setup command ------------------------
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