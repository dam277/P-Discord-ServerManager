import nextcord
import os

# from ...srvm_views.ConfirmationView import ConfirmationView
from ...._commands.Command import Command
from ..Create import Create

from .....database.models.tables.Server import Server
from .....database.models.tables.PrivateChannel import PrivateChannel

from .....utils.enums.permissions.DiscordPermissions import DiscordPermissions

from .....utils.logger.Logger import Logger, LogDefinitions

class CreatePrivateChannel(Create):
    """ # PrivateChannel command class
    
    Description :
    ---
        Manage the PrivateChannel discord command
    
    Access :
    ---
        src.bots.server_manager.srvm_commands.channels.PrivateChannel.py\n
        PrivateChannel
    
    inheritance :
    ---
        - Command : :class:`Command` => Parent class of database commands
    """
    def __init__(self, guild_id: int, channel_name: str):
        """ # PrivateChannel command constructor
        
        Description :
        ---
            Construct a PrivateChannel command object
        
        Access :
        ---
            src.bots.server_manager.srvm_commands.channels.PrivateChannel.py\n
            PrivateChannel.__init__()
        
        Parameters :
        ---
            - guild_id : :class:`int` => Guild id of the command
            - channel_name : :class:`str` => Channel to set as private
        
        Returns :
        ---
            :class:`None`
        """
        self.guild_id = guild_id
        self.channel_name = channel_name
        super().__init__()

    @Command.permissions([DiscordPermissions.manage_guild])
    @Command.register(name="private_channel", description="Create a private channel into the discord server which will make the users able to join it and automatically create a new private category for him", parent="/create", channel_name="Name of the channel")
    async def execute(self, interaction: nextcord.Interaction):
        """ # PrivateChannel command execute method
        
        Description :
        ---
            Execute the PrivateChannel command
        
        Access :
        ---
            src.bots.server_manager.srvm_commands.channels.PrivateChannel.py\n
            PrivateChannel.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Discord interaction with the command
        
        Returns :
        ---
            :class:`None`
        """
        # Execute the parent function
        await super().execute(interaction)
        if not self.has_permission:
            return
        
        # Get the server id
        server_id_result = await Server.get_server_id_by_guild_id(self.guild_id)

        # Check if the server exists
        if server_id_result.get("value") is None or not server_id_result.get("passed"):
            return await interaction.send(f"This server is not registered in the database, use /setup first", ephemeral=True) if server_id_result.get("error") is None else await interaction.send(f"An error occured while getting the server id : {server_id_result.get("error")}", ephemeral=True)
        
        # Check if the channel exists in the database
        private_channel_result = await PrivateChannel.get_channel_by_guild_id(self.guild_id)
        if private_channel_result.get("value") is not None or not private_channel_result.get("passed"):
            return await interaction.send(f"This server already has a private channel", ephemeral=True) if private_channel_result.get("error") is None else await interaction.send(f"An error occured while getting the private channel : {private_channel_result.get("error")}", ephemeral=True)
        
        # Check if the channel already exists in the server
        if nextcord.utils.get(interaction.guild.channels, name=self.channel_name):
            return await interaction.send("This server already have a channel with that name"),
            
        # Create the channel
        channel = await interaction.guild.create_voice_channel(self.channel_name)

        # Add the channel to the database if the channel has been created
        if channel:
            channel_result = await PrivateChannel.create_channel(channel.id, server_id_result.get("value"))
            if channel_result.get("passed"):
                # Set message to the user to confirm the creation of the channel and mention it
                message = f"Channel {channel.mention} has been created"

            # Send message to the user
            return await interaction.send(message)
        
        # Send error message to the user
        return await interaction.send("An error occured while creating the channel")