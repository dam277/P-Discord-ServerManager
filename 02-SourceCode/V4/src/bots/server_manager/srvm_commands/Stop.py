import nextcord
from nextcord.ext import commands
import os

from ....utils.enums.permissions.DiscordPermissions import DiscordPermissions

from ..._commands.Command import Command

class Stop(Command):
    """ # Stop command 
    
    Description :
    ---
        Stop a file to the server
    
    Access :
    ---
        src.bots.server_manager.bot_commands.Stop.py\n
        Stop
    
    Inheritence :
    ---
        :class:`Command`
    """

    def __init__(self):
        """ # Stop command constructor

        Description :
        ---
            Construct a Stop command object
        
        Access : 
        ---
            src.bots.server_manager.bot_commands.Stop.py\n
            Stop.__init__()

        Parameters :
        ---
            - guild_id : :class:`int` => Guild id of the command
            - file : :class:`nextcord.Attachment` => File to Stop

        Returns : 
        ---
            :class:`None`
        """
        super().__init__()

    @Command.register(name="/stop", description="Stop something to the server \n /!\\ This is a parent command which permit to use other subcommand by passing her")
    async def execute(self, interaction: nextcord.Interaction, *args, **kwargs):
        """ # Stop command execute method
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the Stop command
        
        Access :
        ---
            src.bots.server_manager.bot_commands.Stop.py\n
            Stop.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Interaction of the command
        
        Returns :
        ---
            :class:`None`
        """
        pass