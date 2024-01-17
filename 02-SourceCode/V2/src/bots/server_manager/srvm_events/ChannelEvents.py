import nextcord
import os

from ..srvm_views.ConfirmationView import ConfirmationView
from ..._commands.Command import Command

from ..._events.Event import Event
from ....database.models.tables.Server import Server
from ....database.models.tables.PrivateChannel import PrivateChannel

from ....utils.logger.Logger import Logger, LogDefinitions

class ChannelEvents(Event):
    """ # ChannelEvents class
    
    Description :
    ---
        Manage the ChannelEvents discord events
    
    Access :
    ---
        src.bots.server_manager.srvm_events.ChannelEvents.py\n
        ChannelEvents

    inheritance :
    ---
        - Event : :class:`Event` => Parent class of all events
    """
    def __init__(self, channel: nextcord.abc.GuildChannel):
        """ # ChannelEvents constructor
        
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

    async def on_guild_channel_delete(self):
        """ # On guild channel delete event
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Event called when a channel is deleted
        
        Access :
        ---
            src.bots.server_manager.srvm_events.ChannelEvents.py\n
            ChannelEvents.on_guild_channel_delete()
        
        Returns :
        ---
            :class:`None`
        """
        Logger.log(LogDefinitions.INFO, f"{__class__.__name__} event triggered on {self.channel.name} channel deletion")
        # Get the private channel if exists
        private_channel = await PrivateChannel.get_channel_by_channel_id(self.channel.id)
        
        print(private_channel.id)
    