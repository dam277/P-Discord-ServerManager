import nextcord

from .....database.models.tables.Server import Server
from ..Command import Command


class Setup(Command):
    """ Setup command """
    def __init__(self, guild_id: int, name: str):
        """ Setup command class constructor
        $param guild_id: int => id of the guild
        $param name: str => name of the guild"""
        self.guild_id = guild_id
        self.name = name

    async def execute(self, interaction: nextcord.Interaction):
        """ Execute the command 
        $param interaction: nextcord.Interaction => Interaction within the user and the command """
        message = await Server.create_server(guild_id=self.guild_id, name=self.name)
        await interaction.response.send_message(message, ephemeral=True)
