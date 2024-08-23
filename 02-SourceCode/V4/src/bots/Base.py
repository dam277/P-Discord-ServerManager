import json
from abc import ABC, abstractmethod
import nextcord

from ..database.models.srvm_tables.File import File

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
    file_type = FileTypes.DEFAULT
    
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

    def get_precise_time(self, seconds: int) -> str:
        """ # Get precise time function
        
        Description :
        ---
            Get the precise time from seconds

        Access : 
        ---
            src.bots.Base.py\n
            Base.get_precise_time()

        Parameters :
        ---
            seconds : :class:`int` => Time in seconds - format: mm:ss

        Returns : 
        ---
            :class:`str`
        """
        # Setting the units
        minute = 60

        # Calculate the time in minutes and seconds
        minutes = int(str(seconds / minute).split(".")[0])
        seconds -= minutes * minute
        
        if len(str(minutes)) == 1:
            minutes = f"0{minutes}"
        
        if len(str(seconds)) == 1:
            seconds = f"0{seconds}"
        
        # Return the time
        return f"{minutes}:{seconds}"

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

    async def get_file_id_by_type(self, interaction: nextcord.Interaction):
        """ # Get file id by type function
        
        Description :
        ---
            Get the file id by type

        Access : 
        ---
            src.bots.Base.py\n
            Base.get_file_id_by_type()

        Parameters :
        ---
            file_name : :class:`str` => Name of the file

        Returns : 
        ---
            :class:`int`
        """
        if not self.file_name:
            return
        
        # Get the file type
        self.get_file_type(self.file_name)

        # Get the file
        file_result = await File.get_file_by_name_and_guild_id(self.file_name, self.guild_id)

        # Check if the query passed
        if not file_result.get("passed") or file_result.get("object") is None:
            return await interaction.send(f"This file doesn't exists", ephemeral=True) if file_result.get("error") is None else await interaction.send(f"An error occured while getting the file : {file_result.get("error")}", ephemeral=True)
        
        # Get the image
        images_result = await self.file_type.value.get_all_files()
        if not images_result.get("passed") or not images_result.get("objects"):
            return await interaction.send(f"An error occured while getting the image : {images_result.get("error")}", ephemeral=True)
        
        # Check if the file is an image
        if file_result.get("object").id not in [image.id for image in images_result.get("objects")]:
            return await interaction.send(f"This file is not an image", ephemeral=True)
            
        # Set the file
        return file_result.get("object").id