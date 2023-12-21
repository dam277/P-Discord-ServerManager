import discord
from discord.ext import commands
import os
import asyncio
from ..Bot import Bot

class ServerManagerBot(Bot):
    """ Server manager bot class """
    def __init__(self, discord_token):
        command_prefix = "$"
        intents = discord.Intents.all()
        super().__init__(command_prefix, intents, discord_token)

        self.events()

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