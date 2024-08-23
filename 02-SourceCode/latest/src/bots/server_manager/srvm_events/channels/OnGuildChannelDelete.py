import nextcord
import os

from typing import Union

from ...._commands.Command import Command

from ...._events.Event import Event
from .....database.models.srvm_tables.Server import Server
from .....database.models.srvm_tables.Channel import Channel
from .....database.models.srvm_tables.ChannelType import ChannelType

from .....utils.logger.Logger import Logger, LogDefinitions

class OnGuildChannelDelete(Event):
    """ # OnGuildChannelDelete event class
    
    Description :
    ---
        Manage the OnGuildChannelDelete event discord event
        
    Access :
    ---
        src.bots.server_manager.srvm_events.OnGuildChannelDelete.py\n
        OnGuildChannelDelete
    
    inheritance :
    ---
        - Event : :class:`Event` => Parent class of all events
    """
    def __init__(self, channel: nextcord.abc.GuildChannel):
        """ # OnGuildChannelDelete constructor
        
        Description :
        ---
            Construct a ChannelEvents object
        
        Access :
        ---
            src.bots.server_manager.srvm_events.ChannelEvents.py\n
            ChannelEvents.__init__()
        
        Returns :
        ---
            :class:`None`
        """
        self.channel = channel
        super().__init__()

    @Event.trigger(name="on_guild_channel_delete")
    async def execute(self):
        """ # OnGuildChannelDelete event execute method
        
        Description :
        ---
            Execute the OnGuildChannelDelete event
            
        Access :
        ---
            src.bots.server_manager.srvm_events.OnGuildChannelDelete.py\n
            OnGuildChannelDelete.on_guild_channel_delete()
            
        Returns :
        ---
            :class:`None`
        """
       
        # Check if the channel is a special channel
        await self.check_special_channels()

    @Event.trigger(name="special_channels", parent=True)
    async def check_special_channels(self):
        """ # Check special channels

        Description :
        ---
            Check if the deleted channel is a special channel
        
        Access :
        ---
            src.bots.server_manager.srvm_events.OnGuildChannelDelete.py\n
            OnGuildChannelDelete.check_special_channels()

        Returns :
        ---
            :class:`None`
        """
        # Get the Special channel if exists
        channels_result = await Channel.get_channels_by_guild_id(self.channel.guild.id)
        
        # Check if the channel exists
        if not channels_result.get("objects") or not channels_result.get("passed"):
            return
        
        # Get the channels
        channels = channels_result.get("objects")
        
        for channel in channels:
            # Check if the deleted channel is a special channel
            if channel.channelID != self.channel.id:
                continue
            
            # Delete the Special channel from the database
            result = await Channel.delete_channel_by_id(channel.id)

            # Check if the channel has been deleted
            if not result.get("passed"):
                Logger.log(LogDefinitions.ERROR, f"Special channel {channel.channelID}/{self.channel.name} not deleted")
                return
            
            Logger.log(LogDefinitions.SUCCESS, f"Special channel {channel.channelID}/{self.channel.name} deleted")
            return 