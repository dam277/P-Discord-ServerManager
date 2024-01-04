import nextcord
from nextcord.ext import commands
import os

from ...._views.ConfirmationView import ConfirmationView
from ...._commands.Command import Command

from .....database.models.tables.Server import Server
from .....database.models.tables.File import File

from .....utils.logger.Logger import Logger, LogDefinitions

class DeleteFile(Command):
    """ # DeleteFile command class
    
    Description :
    ---
        Manage the DeleteFile discord command
        
    Access :
    ---
        src.bots.server_manager.srvm_commands.files.DeleteFile.py\n
        DeleteFile
        
    inheritance :
    ---
        - Command : :class:`Command` => Parent class of database commands
    """
    def __init__(self, file_name: str, guild_id: int):
        """ # DeleteFile command constructor
        
        Description :
        ---
            Construct a DeleteFile command object
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.files.DeleteFile.py\n
            DeleteFile.__init__()

        Parameters :
        ---
            - file_name : :class:`str` => Name of the file to delete
        
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
            src.bots.server_manager.srvm_commands.files.DeleteFile.py\n
            DeleteFile.execute()
            
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Discord interaction object
            
        Returns :
        ---
            :class:`None`"""
        Logger.log(LogDefinitions.INFO, f"{__class__.__name__} command executed in guild {interaction.user.name}")
        file = await File.get_file_by_name_and_guild_id(self.file_name, self.guild_id)
        
        # Send confirmation message to discord
        confirmation_view = ConfirmationView()
        await interaction.send("Are you sure you want to delete this file ?", view=confirmation_view)
        await confirmation_view.wait()

        # Check if the user confirmed the action, if not, send error message to discord as reply
        if not confirmation_view.value:
            await interaction.send(f"The file **'{self.file_name}'** was not deleted !")
            return

        # Check if the file exists in database, if not, send error message to discord as reply
        if file is None:
            await interaction.send(f"The file **'{self.file_name}'** does not exists in database !")
            return
        
        # Get the file type
        self.get_file_type(file.name)
        print(self.file_type)

        # Delete the file from the database
        message = await self.file_type.value.delete_file_by_id(file.id)

        # Check if the path exists, if not, send error message to discord as reply
        if not os.path.exists(file.path):
            await interaction.send(f"The file **'{self.file_name}'** does not exists in server !")
            return
        
        # Delete the file from the server
        os.remove(file.path)
        Logger.log(LogDefinitions.INFO, f"File {file.path} has been deleted from server")

        # Send success message to discord as reply
        await interaction.send(content=message.replace("[file_name]", self.file_name))
        return
        
        
        
