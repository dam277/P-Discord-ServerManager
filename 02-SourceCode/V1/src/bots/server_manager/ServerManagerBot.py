import nextcord
from nextcord.ext import commands
from colorama import Fore

from ..Bot import Bot
from .bot_commands.setup.Setup import Setup
from .bot_commands.cmds.GetCommands import GetCommands
from .bot_commands.files.AddFile import AddFile
from .bot_commands.files.DeleteFile import DeleteFile 
from .bot_autocompletes.files.FileAutocomplete import FileAutocomplete
from ...modules.logger.Logger import Logger, LogDefinitions

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

        # ---- Setup command ------------------------
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

        # ---- Get commands command ------------------------
        @self.bot_instance.slash_command(name="get_commands", description="Get all the usable commands of the bot")
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

        #region ---- Add commands ------------------------
        @self.bot_instance.slash_command(name="add", description="Add something")
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
        #endregion ---- subcommands ------------------------
        #endregion ---- Add commands ------------------------

        #region ---- Delete commands ------------------------
        @self.bot_instance.slash_command(name="delete", description="Delete something")
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
            command = DeleteFile(interaction.guild.id, file_name)
            await command.execute(interaction)
            
        # Create autocomplete function for delete file subcommand
        @delete_file.on_autocomplete("file_name")
        async def delete_file_autocomplete(interaction: nextcord.Interaction, file_name: str):
            """ Bot delete file autocomplete function
            /!\\ This is a coroutine, it needs to be awaited

            Description :
            ---
                Autocomplete function for the delete file subcommand
            
            Access :
            ---
                src.bots.server_manager.ServerManagerBot.py\n
                ServerManagerBot.slash_commands(delete_file_autocomplete())

            Parameters:
                interaction :class:`nextcord.Interaction`: The interaction object representing the user's interaction with the bot.
            
            Returns:
                :class:`None`
            """
            autocomplete = FileAutocomplete(file_name, interaction.guild.id)
            return await autocomplete.execute(interaction)
        #endregion ---- subcommands ------------------------
        #endregion ---- Delete commands ------------------------
        
