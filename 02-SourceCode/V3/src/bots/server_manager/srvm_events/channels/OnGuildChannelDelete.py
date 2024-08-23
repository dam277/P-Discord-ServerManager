import nextcord
import os

#from ..srvm_views.ConfirmationView import ConfirmationView
from ...._commands.Command import Command

from ...._events.Event import Event
from .....database.models.tables.Server import Server
from .....database.models.tables.PrivateChannel import PrivateChannel

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
        await self.check_private_channel()

    @Event.trigger(name="private_channel", parent=True)
    async def check_private_channel(self):
        # Get the private channel if exists
        private_channel_result = await PrivateChannel.get_channel_by_guild_id(self.channel.guild.id)
        
        # Check if the channel exists
        if not private_channel_result.get("object") or not private_channel_result.get("passed"):
            return
        
        # Check if the deleted channel is the private channel
        if private_channel_result.get("object").channelID != self.channel.id:
            return
        
        # Delete the private channel from the database
        result = await PrivateChannel.delete_channel_by_id(private_channel_result.get("object").id)

        # Check if the channel has been deleted
        if not result.get("passed"):
            Logger.log(LogDefinitions.ERROR, f"Private channel {private_channel_result.get('object').channelID}/{self.channel.name} not deleted")
            return
        
        Logger.log(LogDefinitions.SUCCESS, f"Private channel {private_channel_result.get('object').channelID}/{self.channel.name} deleted")
        return 