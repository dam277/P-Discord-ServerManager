from enum import Enum

from ...bots.server_manager.srvm_events import OnGuildChannelDelete, OnVoiceStateUpdate

class Events(Enum):
    on_guild_channel_delete = OnGuildChannelDelete
    on_voice_state_update = OnVoiceStateUpdate