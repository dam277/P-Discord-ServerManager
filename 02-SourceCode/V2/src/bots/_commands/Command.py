import json
from abc import ABC, abstractmethod
import nextcord

from ...utils.enums.FileTypes import FileTypes

from ...database.models.Table import Table

class Command(ABC):
    """ # Command class
        
    Description :
    ---
        Manage commands as a parent of all of them

    Access : 
    ---
        src.bots.server_manager.commands.Command.py\n
        Command
    """
    # Shared class variables
    file_type = None
    
    def __init__(self):
        """ # Command class constructor
        
        Description :
        ---
            Construct a base command and get the setting as a self variable
        
        Access : 
        ---
            src.bots.commands.Command.py\n
            Command

        Returns : 
        ---
            :class:`None`
        """
        s = open("src/resources/configs/settings.json")
        
        self.settings = json.load(s)

    @abstractmethod
    async def execute(self, interation: nextcord.Interaction):
        """ # Command class execute method
        
        Description :
        ---
            Execute the command

        Access : 
        ---
            src.bots.commands.Command.py\n
            Command.execute()

        Parameters :
        ---
            interation : :class:`nextcord.Interaction`

        Returns : 
        ---
            :class:`None`
        """
        pass

    def get_file_type(self, file_name):
        """ # Get file type function
        
        Description :
        ---
            Get the type of the file

        Access : 
        ---
            src.bots.commands.Command.py\n
            Command.get_file_type()

        Parameters :
        ---
            file_name : :class:`str` => Name of the file

        Returns : 
        ---
            :class:`FileTypes`
        """
        # Get the extension of the file
        extension = file_name.split(".")[-1].lower()

        # Set the file type depending on the extension
        if extension in self.settings["resources"]["extensions"]["image"]:
            self.file_type = FileTypes.IMAGE
        elif extension in self.settings["resources"]["extensions"]["music"]:
            self.file_type = FileTypes.MUSIC
        else:
            self.file_type = FileTypes.DEFAULT

    async def check_object_type(self, object: Table, type: type, name: str, interaction: nextcord.Interaction, search: bool = True) -> bool:
        """ # Check object type function
        
        Description :
        ---
            Check if the object is of the type

        Access : 
        ---
            src.bots.commands.Command.py\n
            Command.check_object_type()

        Parameters :
        ---
            object : :class:`Table` => Object to check
            type : :class:`type` => Type to check

        Returns : 
        ---
            :class:`bool`
        """
                # Check if note list exists
        # Check if the object is of the type
        if not isinstance(object, type):
            # Send a message if the object is not of the type
            if not search:
                return False
            # Send a message if the object is none 
            if object is None:
                await interaction.send(f"Element **{name}** not found")
                return False
            await interaction.send(object)
            return False
        return True