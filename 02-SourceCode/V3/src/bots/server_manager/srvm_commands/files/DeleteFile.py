import nextcord
from nextcord.ext import commands
import os

from ....server_manager.srvm_views.ConfirmationView import ConfirmationView
from ...._commands.Command import Command
from ..Delete import Delete

from .....database.models.tables.Server import Server
from .....database.models.tables.File import File

from .....utils.logger.Logger import Logger, LogDefinitions

class DeleteFile(Delete):
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
    
    @Command.register(name="delete_file", description="Delete a file from the server", parent="/delete", file_name="Name of the file to delete")
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
        # Execute the parent function
        await super().execute(interaction)
        if not self.has_permission:
            return
        
        # Get the file by name and guild id
        file_result = await File.get_file_by_name_and_guild_id(self.file_name, self.guild_id)

        # Check if the file exists
        if file_result.get("object") is None:
            await interaction.send("File doesn't exist", ephemeral=True)
            return

        # Get the file
        file = file_result.get("object")

        # Check if the user confirmed the action, if not, send error message to discord as reply
        confirmation_view = ConfirmationView()
        await confirmation_view.execute(interaction, "Are you sure you want to delete this file ?")

        # Check if the user confirmed
        if not confirmation_view.value:
            await interaction.send(f"The file **'{self.file_name}'** deletion has been canceled !")
            return
        
        # Get the file type
        self.get_file_type(file.name)
        delete_result = await self.file_type.value.delete_file_by_id(file.id)

        if not delete_result.get("passed"):
            await interaction.send("An error occured while deleting the file from the database !")
            Logger.log(LogDefinitions.ERROR, delete_result.get("error"))
            return

        # Check if the query passed
        await interaction.send("File deleted from database !")

        # Check if the path exists, if not, send error message to discord as reply
        if not os.path.exists(file.path):
            await interaction.followup.send(f"The file **'{self.file_name}'** does not exists in files !")
            return
        
        # Delete the file from the server
        os.remove(file.path)

        # Send success message to discord as reply
        await interaction.send(content=f"The file **'{self.file_name}'** has been deleted !")
        return