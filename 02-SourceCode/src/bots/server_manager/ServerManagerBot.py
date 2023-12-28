import nextcord
from nextcord.ext import commands
import os
import asyncio
from ..Bot import Bot
from .commands.setup.Setup import Setup

class ServerManagerBot(Bot):
    """ Server manager bot class 
    $inherits: Bot"""
    def __init__(self, discord_token):
        """ Constructor of server manager bot
        $param discord_token: str => token of the discord bot """
        command_prefix = "$"                                        # Set command prefix
        intents = nextcord.Intents.all()                            # Set the intents list

        # Set the datas into the parent
        super().__init__(command_prefix, intents, discord_token)

        # Setup bot interactions
        self.events()
        self.regular_commands()
        self.slash_commands()

    def events(self):
        """ Events of the bot """
        @self.bot_instance.event
        async def on_message(message: nextcord.Message):
            print(f"{message.author} : {message.content}")
            if message.author.bot:
                return
            
    def regular_commands(self):
        """ regular commands of the bot """

    def slash_commands(self):
        """ServerManagerBot.slash_commands()

        Description :
            Slash commands of the bot

        $Returns : 
            None
        """

        # ---- Setup command ------------------------
        @self.bot_instance.slash_command(name="setup", description="Setup the server into the database")
        async def setup(interaction: nextcord.Interaction):
            """
            # Bot setup command
            ## Access
                ServerManagerBot.slash_commands(setup())

            ## Description :
                Setup the actual discord server (guild) into the database

            ## Parameters : 
                - interaction : nextcord.Interaction => Interaction with the user

            ## Returns : 
                None
            """
            # Create object of the command with the datas
            command = Setup(interaction.guild.id, interaction.guild.name)
            await command.execute(interaction)

        @self.bot_instance.slash_command(name="get_commands", description="Get all the usable commands of the bot")
        async def get_commands(interaction: nextcord.Interaction):
            """ServerManagerBot.slash_commands(get_commands())

            Description :
                Get the commands of the bot

            $Parameters : 
                - interaction : nextcord.Interaction => Interaction with the user

            $Returns : 
                None
            """