from discord import Object
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

    async def execute(self, interaction: nextcord.Interaction, objects: list, attributes: str = None, separator: str = "-"):
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

        # Check if the objects exists and join the attributes to create the name
        if objects:
            for object in objects:
                name = "".join((str(getattr(object, attribute)).lower() + separator) for attribute in attributes)[:-1] if attributes else str(object).lower()
                if self.current.lower() in name:
                    values.append(name)

        # Send the autocomplete
        await interaction.response.send_autocomplete(values)