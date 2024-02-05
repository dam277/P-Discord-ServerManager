import nextcord
import os

from ...._autocompletes.Autocomplete import Autocomplete

from .....database.models.srvm_tables.Server import Server
from .....database.models.srvm_tables.ChannelType import ChannelType

class ChannelTypeAutocomplete(Autocomplete):
    """ # ChannelTypeAutocomplete autocomplete class
    
    Description :
    ---
        Manage the ChannelTypeAutocomplete discord autocomplete
        
    Access :
    ---
        src.bots.server_manager.srvm_autocompletes.ChannelTypes.ChannelTypeAutocomplete.py\n
        ChannelTypeAutocomplete
        
    inheritance :
    ---
        - autocomplete : :class:`autocomplete` => Parent class of database autocompletes"""
    def __init__(self, current: str, guild_id: int):
        """ # ChannelTypeAutocomplete autocomplete constructor
        
        Description :
        ---
            Construct a ChannelTypeAutocomplete autocomplete object
            
        Access :
        ---
            src.bots.server_manager.srvm_autocompletes.ChannelTypes.ChannelTypeAutocomplete.py\n
            ChannelTypeAutocomplete.__init__()
        
        Parameters :
        ---
            - current : :class:`str` => Current string of the autocomplete
            - guild_id : :class:`int` => Guild id of the autocomplete
            
        Returns :
        ---
            :class:`None`
        """
        self.guild_id = guild_id

        super().__init__(current)

    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute autocomplete function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the autocomplete and make all connections with models and frontend (discord chat)       
            
        Access :
        ---
            src.bots.server_manager.srvm_autocompletes.ChannelTypes.ChannelTypeAutocomplete.py\n
            ChannelTypeAutocomplete.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Nextcord interaction object
            
        Returns :
        ---
            :class:`None`
        """
        # Get the ChannelType list
        channelTypes_result = await ChannelType.get_all_channel_types()

        # Check if the result is empty
        if channelTypes_result.get("objects"):
            # Execute the autocomplete
            await super().execute(interaction, channelTypes_result.get("objects"), "name")
            return
        
        # Send empty autocomplete
        await interaction.response.send_autocomplete([])