import nextcord
import os

from ...srvm_views.ConfirmationView import ConfirmationView
from ...._commands.Command import Command

from .....database.models.tables.Server import Server
from .....database.models.tables.PrivateChannel import PrivateChannel

from .....utils.logger.Logger import Logger, LogDefinitions

class CreatePrivateChannel(Command):
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

    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute command function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the command and make all connections with models and frontend (discord chat)
        
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
        Logger.log(LogDefinitions.INFO, f"{__class__.__name__} command called by {interaction.user.name}")
        
        # Get the server id
        server_id = await Server.get_server_id_by_guild_id(self.guild_id)

        # Check if the server is registered
        if type(server_id) is not int:
            await interaction.send("This server is not registered make /setup first"),
            return
        
        # Check if the server exists
        private_channel = await PrivateChannel.get_channel_by_guild_id(server_id)

        # Check if the server already has a private channel
        if private_channel:
            await interaction.send("This server already has a private channel"),
            return
        
        # Check if the channel already exists
        if nextcord.utils.get(interaction.guild.channels, name=self.channel_name):
            await interaction.send("This channel already exists"),
            return
        
        # Create the channel
        channel = await interaction.guild.create_voice_channel(self.channel_name)

        # Add the channel to the database if the channel has been created
        if channel:
            message = await PrivateChannel.create_channel(channel.id, server_id)
            if not message:
                # Set message to the user to confirm the creation of the channel and mention it
                message = f"Channel {channel.mention} has been created"

            # Send message to the user
            await interaction.send(message)

           
