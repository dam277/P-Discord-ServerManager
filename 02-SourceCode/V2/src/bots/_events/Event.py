import json
from abc import ABC, abstractmethod
import nextcord

class Event(ABC):
    def __init__(self, current: str = ""):
        """ # Event base constructor

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