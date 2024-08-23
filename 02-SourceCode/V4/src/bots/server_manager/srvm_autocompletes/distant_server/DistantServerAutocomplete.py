import nextcord
import os

from .....database.models.srvm_tables.DistantServer import DistantServer

from ...._autocompletes.Autocomplete import Autocomplete

from .....database.models.srvm_tables.Server import Server
from .....database.models.srvm_tables.ChannelType import ChannelType

class DistantServerAutocomplete(Autocomplete):
    """ # DistantServerAutocomplete autocomplete class
    
    Description :
    ---
        Manage the DistantServerAutocomplete discord autocomplete
        
    Access :
    ---
        src.bots.server_manager.srvm_autocompletes.ChannelTypes.DistantServerAutocomplete.py\n
        DistantServerAutocomplete
        
    inheritance :
    ---
        - autocomplete : :class:`autocomplete` => Parent class of database autocompletes"""
    def __init__(self, current: str, guild_id: int):
        """ # DistantServerAutocomplete autocomplete constructor
        
        Description :
        ---
            Construct a DistantServerAutocomplete autocomplete object
            
        Access :
        ---
            src.bots.server_manager.srvm_autocompletes.ChannelTypes.DistantServerAutocomplete.py\n
            DistantServerAutocomplete.__init__()
        
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
            src.bots.server_manager.srvm_autocompletes.ChannelTypes.DistantServerAutocomplete.py\n
            DistantServerAutocomplete.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Nextcord interaction object
            
        Returns :
        ---
            :class:`None`
        """
        # Get the ChannelType list
        distant_servers_result = await DistantServer.get_distant_servers_by_guild_id(self.guild_id)

        # Check if the result is empty
        if distant_servers_result.get("objects"):
            # Execute the autocomplete
            await super().execute(interaction, distant_servers_result.get("objects"), ["adress", "port"], ":")
            return
        
        # Send empty autocomplete
        await interaction.response.send_autocomplete([])