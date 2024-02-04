import nextcord
from nextcord.ext import commands
import os

from ...._commands.Command import Command
from ..Get import Get

from .....database.models.tables.File import File

from .....utils.logger.Logger import Logger, LogDefinitions

class GetFile(Get):
    """ # GetFile command class
    
    Description :
    ---
        Manage the GetFile discord command
        
    Access :
    ---
        src.bots.server_manager.srvm_commands.files.GetFile.py\n
        GetFile
        
    inheritance :
    ---
        - Get : :class:`Get` => Parent class of database commands
    """
    def __init__(self, file_name: str, guild_id: int):
        """ # GetFile command constructor
        
        Description :
        ---
            Construct a GetFile command object
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.files.GetFile.py\n
            GetFile.__init__()

        Parameters :
        ---
            - file_name : :class:`str` => Name of the file to get
        
        Returns :
        ---
            :class:`None`"""
        self.file_name = file_name
        self.guild_id = guild_id

        super().__init__()
    
    @Command.register(name="get_file", description="Get a file from the server which has been added before", parent="/get", file_name="Name of the file to get and send to the channel")
    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute command function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the command and make all connections with models and frontend (discord chat)
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.files.GetFile.py\n
            GetFile.execute()
            
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Discord interaction object
            
        Returns :
        ---
            :class:`None`
        """
        # Execute the parent function
        await super().execute(interaction)
        if not self.has_permission:
            return
        
        # Get the file from the database
        file_result = await File.get_file_by_name_and_guild_id(self.file_name, self.guild_id)

        # Check if the function has passed, if not, send error message to discord as reply
        if not file_result.get("passed"):
            return await interaction.send(f"An error occured : {file_result.get("error")}", ephemeral=True)
        
        # Check if the file exists, if not, send error message to discord as reply
        if not file_result.get("object"):
            return await interaction.send("This file doesn't exist", ephemeral=True)
        
        # Check if the path exists, if not, send error message to discord as reply
        if not os.path.exists(file_result.get("object").path):
            return await interaction.send(f"The file **'{self.file_name}'** does not exists in server !")
        
        # Check if the file isn't too big, if not, send error message to discord as reply
        if os.path.getsize(file_result.get("object").path) > self.settings["resources"]["max_file_size"]:
            return await interaction.send(f"The file **'{self.file_name}'** is too big to be send !")
            
        # Send the file to discord
        await interaction.send(content="Here is the file you asked", file=nextcord.File(file_result.get("object").path))