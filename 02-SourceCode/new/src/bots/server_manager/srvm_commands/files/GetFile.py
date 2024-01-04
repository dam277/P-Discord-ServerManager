import nextcord
from nextcord.ext import commands
import os

from ...._commands.Command import Command

from .....database.models.tables.File import File

from .....utils.logger.Logger import Logger, LogDefinitions

class GetFile(Command):
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
        - Command : :class:`Command` => Parent class of database commands
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
            :class:`None`"""
        Logger.log(LogDefinitions.INFO, f"GetFile command called by {interaction.user.name}")
        file = await File.get_file_by_name_and_guild_id(self.file_name, self.guild_id)
        
        # Check if the file exists in database, if not, send error message to discord as reply
        if file is None:
            await interaction.send(f"The file **'{self.file_name}'** does not exists in database !")
            return

        # Check if the path exists, if not, send error message to discord as reply
        if not os.path.exists(file.path):
            await interaction.send(f"The file **'{self.file_name}'** does not exists in server !")
            return
        
        # Check if the file isn't too big, if not, send error message to discord as reply
        if os.path.getsize(file.path) > self.settings["resources"]["max_file_size"]:
            await interaction.send(f"The file **'{self.file_name}'** is too big to be send !")
            return
        
        # Send the file to discord
        await interaction.send(content="Here is the file you asked", file=nextcord.File(file.path))