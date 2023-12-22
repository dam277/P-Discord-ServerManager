import discord
from discord.ext import commands
import os
import asyncio
from ..Bot import Bot

class ServerManagerBot(Bot):
    """ Server manager bot class 
    $inherits: Bot"""
    def __init__(self, discord_token):
        """ Constructor of server manager bot
        $param discord_token: str => token of the discord bot """
        command_prefix = "$"                                        # Set command prefix
        intents = discord.Intents.all()                             # Set the intents list
        
        # Set the datas into the parent
        super().__init__(command_prefix, intents, discord_token)

        # Setup bot interactions
        self.events()
        self.regular_commands()
        self.slash_commands()

    def events(self):
        """ Events of the bot """
        @self.bot_instance.event
        async def on_message(message: discord.Message):
            print(f"{message.author} : {message.content}")
            if message.author.bot:
                return
            
    def regular_commands(self):
        """ regular commands of the bot """

    def slash_commands(self):
        """ slash commands of the bot """