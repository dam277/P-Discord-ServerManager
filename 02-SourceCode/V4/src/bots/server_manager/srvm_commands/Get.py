import nextcord
from nextcord.ext import commands
import os

from ....utils.enums.permissions.DiscordPermissions import DiscordPermissions

from ..._commands.Command import Command

class Get(Command):
    """ # Get command 
    
    Description :
    ---
        Get a file to the server
    
    Access :
    ---
        src.bots.server_manager.bot_commands.Get.py\n
        Get
    
    Inheritence :
    ---
        :class:`Command`
    """

    def __init__(self):
        """ # Get command constructor

        Description :
        ---
            Construct a Get command object
        
        Access : 
        ---
            src.bots.server_manager.bot_commands.Get.py\n
            Get.__init__()

        Parameters :
        ---
            - guild_id : :class:`int` => Guild id of the command
            - file : :class:`nextcord.Attachment` => File to Get

        Returns : 
        ---
            :class:`None`
        """
        super().__init__()

    #@Command.permissions([DiscordPermissions.administrator])
    @Command.register(name="/get", description="Get something to the server \n /!\\ This is a parent command which permit to use other subcommand by passing her")
    async def execute(self, interaction: nextcord.Interaction, *args, **kwargs):
        """ # Get command execute method
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the Get command
        
        Access :
        ---
            src.bots.server_manager.bot_commands.Get.py\n
            Get.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Interaction of the command
        
        Returns :
        ---
            :class:`None`
        """
        pass