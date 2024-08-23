import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv

from ..utils.logger.Logger import Logger, LogDefinitions

class Bot:
    """ # Bot parent class
        
    Description :
    ---
        Manage all discord bots with this base bot class

    Access : 
    ---
        src.bots.Bot.py\n
        Bot
    """
    def __init__(self, command_prefix: str, intents: nextcord.Intents, discord_token: str):
        """ # Bot class constructor
        
        Description :
        ---
            Construct a bot object to manage discord bot
        
        Access : 
        ---
            src.bots.Bot.py\n
            Bot.__init__()

        Parameters : 
        ---
            - command_prefix : :class:`str` => Discord bot command prefix
            - intents : :class:`nextcord.Intents` => Discord bot intents
            - discord_token : :class:`str` => Discord bot token

        Returns : 
        ---
            :class:`None`
        """
        Logger.log(LogDefinitions.INFO, f"Bot initiated")

        # Get the configs and set the bot instance as a commands.Bot object from discord
        load_dotenv()
        self.configs = {"discord_token": discord_token, "db_host": os.getenv("DB_HOST"), "db_port": os.getenv("DB_PORT"), "db_user": os.getenv("DB_USER"), "db_password" : os.getenv("DB_PASSWORD"), "db_name": os.getenv("DB_NAME")}
        self.bot_instance = commands.Bot(command_prefix=command_prefix, intents=intents)
        
        # Setup the bots shared interactions
        self.shared_events()
        self.shared_regular_commands()
        self.shared_slash_commands()

    def shared_events(self):
        """ # Shared events of the bots
        
        Description :
        ---
            Setup the shared events for the bots that inherit to this class
        
        Access : 
        ---
            src.bots.Bot.py\n
            Bot.shared_events()
            
        Returns : 
        ---
            :class:`None`
        """
        @self.bot_instance.event
        async def on_ready():
            """ # On bot ready event
            /!\\ This is a coroutine, it needs to be awaited
        
            Description :
            ---
                Subfunction of shared_events\n
                Calls when the bot is ready to be connected to discord
            
            Access : 
            ---
                src.bots.Bot.py\n
                Bot.shared_events(on_ready())
                
            Returns : 
            ---
                :class:`None`
            """
            Logger.log(LogDefinitions.INFO, f"Bot is logged on as {self.bot_instance.user}")
            try:
                # Sync the commands and get a list of them
                await self.bot_instance.sync_application_commands()

                # Get all commands from the bot
                synced_commands = self.bot_instance.get_application_commands()
                Logger.log(LogDefinitions.SUCCESS, f"Synced {len(synced_commands)} commands")
            except Exception as e:
                Logger.log(LogDefinitions.ERROR, e)

    def shared_regular_commands(self):
        """ # Shared regular commands of the bots
        
        Description :
        ---
            Setup the shared the regular commands for the bots that inherit to this class
        
        Access : 
        ---
            src.bots.Bot.py\n
            Bot.shared_regular_commands()
            
        Returns : 
        ---
            :class:`None`
        """

    def shared_slash_commands(self):
        """ # Shared the slash commands of the bots
        
        Description :
        ---
            Setup the shared the slash commands for the bots that inherit to this class
        
        Access : 
        ---
            src.bots.Bot.py\n
            Bot.shared_slash_commands()
            
        Returns : 
        ---
            :class:`None`
        """

    def run(self):
        """ # Bot run function
        
        Description :
        ---
            Start a discord bot to use it on discord
        
        Access : 
        ---
            src.bots.Bot.py\n
            Bot.run()
            
        Returns : 
        ---
            :class:`None`
        """
        self.bot_instance.run(self.configs["discord_token"])