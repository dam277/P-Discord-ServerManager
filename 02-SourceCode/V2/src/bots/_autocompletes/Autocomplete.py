import json
from abc import ABC, abstractmethod
import nextcord

class Autocomplete(ABC):
    """ # Autocomplete base class

    Description :
    ---
        Manage the discord autocompletes

    Access :
    ---
        src.bots.server_manager.autocompletes.Autocomplete.py\n
        Autocomplete

    
    """
    def __init__(self, current: str = ""):
        """ # Autocomplete base constructor

        Description :
        ---
            Construct a Autocomplete object

        Access :
        ---
            src.bots.server_manager.autocompletes.Autocomplete.py\n
            Autocomplete.__init__()
        
        Parameters :
        ---
            current : :class:`str`

        Returns :
        ---
            :class:`None`
        """
        s = open("src/resources/configs/settings.json")
        
        self.current = current
        self.settings = json.load(s)

    @abstractmethod
    async def execute(self, interation: nextcord.Interaction):
        """ # Autocomplete base execute method

        Description :
        ---
            Execute the autocomplete

        Access :
        ---
            src.bots.server_manager.autocompletes.Autocomplete.py\n
            Autocomplete.execute()

        Parameters:
        ---
            interation : :class:`nextcord.Interaction`

        Returns :
        ---
            :class:`None`
        """
        pass