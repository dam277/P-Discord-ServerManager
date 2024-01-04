import nextcord
from nextcord.ext import commands
import os

from ...bot_views.ConfirmationView import ConfirmationView
from ....commands.Command import Command
from .....database.models.tables.Server import Server
from .....modules.logger.Logger import Logger, LogDefinitions

class DeleteFile(Command):
    """ # DeleteFile command class
    
    Description :
    ---
        Manage the DeleteFile discord command
        
    Access :
    ---
        src.bots.server_manager.bot_commands.files.DeleteFile.py\n
        DeleteFile
        
    inheritance :
    ---
        - Command : :class:`Command` => Parent class of database commands
    """
    def __init__(self):
        """ # DeleteFile command constructor
        
        Description :
        ---
            Construct a DeleteFile command object
            
        Access :
        ---
            src.bots.server_manager.bot_commands.files.DeleteFile.py\n
            DeleteFile.__init__()
        
        Returns :
        ---
            :class:`None`"""
        super().__init__()
    
    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute command function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the command and make all connections with models and frontend (discord chat)
            
        Access :
        ---
            src.bots.server_manager.bot_commands.files.DeleteFile.py\n
            DeleteFile.execute()
            
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Discord interaction object
            
        Returns :
        ---
            :class:`None`"""
        Logger.log(LogDefinitions.INFO, f"DeleteFile command called by {interaction.user.name}")
        
        
        
