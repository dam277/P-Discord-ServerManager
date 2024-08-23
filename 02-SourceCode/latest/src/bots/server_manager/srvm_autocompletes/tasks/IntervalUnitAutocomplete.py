import nextcord

from .....utils.enums.IntervalUnits import IntervalUnits

from .....utils.enums.Tasks import Tasks

from ...._autocompletes.Autocomplete import Autocomplete

class IntervalUnitAutocomplete(Autocomplete):
    """ # IntervalUnitAutocompletet autocomplete class
    
    Description :
    ---
        Manage the IntervalUnitAutocompletet discord autocomplete
        
    Access :
    ---
        src.bots.server_manager.srvm_autocompletes.ChannelTypes.IntervalUnitAutocompletet.py\n
        IntervalUnitAutocompletet
        
    inheritance :
    ---
        - autocomplete : :class:`autocomplete` => Parent class of database autocompletes"""
    def __init__(self, current: str):
        """ # IntervalUnitAutocompletet autocomplete constructor
        
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
        # Get the tasks
        tasks_list = IntervalUnits.get_all()
        
        # Check if the result is empty
        if tasks_list:
            # Execute the autocomplete
            await super().execute(interaction, tasks_list)
            return
        
        # Send empty autocomplete
        await interaction.response.send_autocomplete([])