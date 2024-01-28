import json
from abc import ABC, abstractmethod
import nextcord

import asyncio

from ..utils.enums.FileTypes import FileTypes

class Base(ABC):
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
        """ # Base class constructor
        
        Description :
        ---
            Construct a base Base and get the setting as a self variable
        
        Access : 
        ---
            src.bots.Base.py\n
            Base

        Returns : 
        ---
            :class:`None`
        """
        s = open("src/resources/configs/settings.json")
        
        self.settings = json.load(s)

    @abstractmethod
    async def execute(self, interation: nextcord.Interaction):
        """ # Base class execute method
        
        Description :
        ---
            Execute the Base

        Access : 
        ---
            src.bots.Base.py\n
            Base.execute()

        Parameters :
        ---
            interation : :class:`nextcord.Interaction`

        Returns : 
        ---
            :class:`None`
        """
        pass
    
    async def permission_denied(self, interaction: nextcord.Interaction):
        """ # Permission denied function
        
        Description :
        ---
            Send a message to the user to tell him he doesn't have the permission to execute the command

        Access : 
        ---
            src.bots.Base.py\n
            Base.permission_denied()

        Parameters :
        ---
            interaction : :class:`nextcord.Interaction`

        Returns : 
        ---
            :class:`None`
        """
        return await interaction.followup.send("You don't have the permission to execute this command", ephemeral=True) if interaction.response.is_done() else await interaction.send("You don't have the permission to execute this command", ephemeral=True)
    
    async def delete_category(self, category: nextcord.CategoryChannel):
            """ # Delete category function

            Description :
            ---
                Delete the category of the user

            Access :
            ---
                src.bots.server_manager.srvm_events.OnVoiceStateUpdate.py\n
                OnVoiceStateUpdate.on_voice_channel_leave.delete_category()

            Returns :
            ---
                :class:`None`
            """
            # Delete all the category channels
            for channel in category.channels:
                await channel.delete()

            # Delete the category
            await category.delete()

    def get_file_type(self, file_name: str):
        """ # Get file type function
        
        Description :
        ---
            Get the type of the file

        Access : 
        ---
            src.bots.Base.py\n
            Base.get_file_type()

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
