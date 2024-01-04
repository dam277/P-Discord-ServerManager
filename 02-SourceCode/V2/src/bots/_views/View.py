import json
from abc import ABC, abstractmethod
import nextcord

class View(ABC):
    """ # View class
        
    Description :
    ---
        Manage Views as a parent of all of them

    Access : 
    ---
        src.bots.server_manager.wiews.View.py\n
        View
    """
    def __init__(self):
        """ # View class constructor
        
        Description :
        ---
            Construct a base View and get the settings as a self variable
        
        Access : 
        ---
            src.bots.wiews.View.py\n
            View

        Returns : 
        ---
            :class:`None`
        """
        s = open("src/resources/configs/settings.json")

        self.children = []
        self.settings = json.load(s)