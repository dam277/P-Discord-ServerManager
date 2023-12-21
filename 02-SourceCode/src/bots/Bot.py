import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from ..modules.logger import Logger as lg

class Bot:
    def __init__(self, command_prefix: str, intents: discord.Intents, discord_token):
        lg.Logger.log(lg.LogDefinitions.INFO, f"Bot initiated")

        load_dotenv()
        self.configs = {"discord_token": discord_token, "db_host": os.getenv("DB_HOST"), "db_port": os.getenv("DB_PORT"), "db_user": os.getenv("DB_USER"), "db_password" : os.getenv("DB_PASSWORD"), "db_name": os.getenv("DB_NAME")}
        self.bot_instance = commands.Bot(command_prefix=command_prefix, intents=intents)
        
        self.shared_events()

    def shared_events(self):
        """ shared events of the bots """
        @self.bot_instance.event
        async def on_ready():
            lg.Logger.log(lg.LogDefinitions.INFO, f"Bot is logged on as {self.bot_instance.user}")
            try:
                # Get the commands to sync
                synced_commands = await self.bot_instance.tree.sync()
                lg.Logger.log(lg.LogDefinitions.SUCCESS, f"Synced {len(synced_commands)} commands")
            except Exception as e:
                lg.Logger.log(lg.LogDefinitions.ERROR, e)

    def shared_regular_commands(self):
        """ shared regular commands of the bots """

    def shared_slash_commands(self):
        """ shared slash commands of the bots """

    def run(self):
        """ Run the bot """
        self.bot_instance.run(self.configs["discord_token"])