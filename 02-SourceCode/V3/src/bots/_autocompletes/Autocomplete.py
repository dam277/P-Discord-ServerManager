import json
import nextcord

from ..Base import Base

class Autocomplete(Base):
    """ # Autocomplete class
    
    Description :
    ---
        Autocomplete class is the base for all autocomplete commands

    Attributes :
    ---
        settings : :class:`dict`
            The settings of the bot
    """
    def __init__(self, current: str):
        self.current = current
        
        super().__init__()

    async def execute(self, interaction: nextcord.Interaction, objects: list, attribute: str):
        """ # Execute autocomplete function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the autocomplete and make all connections with models and frontend (discord chat)       
            
        Access :
        ---
            src.bots.server_manager.srvm_autocompletes.Autocomplete.py\n
            Autocomplete.execute()
            
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Interaction within the user and the autocomplete
        
        Returns :
        ---
            :class:`None`
        """
                    # Check if the files exists
        # Set the default value
        values = []

        # Check if the objects exists
        if objects:
            values = [getattr(object, attribute)[:100] for object in objects if self.current.lower() in getattr(object, attribute).lower()][:25]

        # Send the autocomplete
        await interaction.response.send_autocomplete(values)