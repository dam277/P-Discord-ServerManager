import nextcord
from nextcord.ext import commands
import os

from ....utils.enums.permissions.DiscordPermissions import DiscordPermissions

from ..._commands.Command import Command

class Start(Command):
    """ # Start command 
    
    Description :
    ---
        Start a file to the server
    
    Access :
    ---
        src.bots.server_manager.bot_commands.Start.py\n
        Start
    
    Inheritence :
    ---
        :class:`Command`
    """

    def __init__(self):
        """ # Start command constructor

        Description :
        ---
            Construct a Start command object
        
        Access : 
        ---
            src.bots.server_manager.bot_commands.Start.py\n
            Start.__init__()

        Parameters :
        ---
            - guild_id : :class:`int` => Guild id of the command
            - file : :class:`nextcord.Attachment` => File to Start

        Returns : 
        ---
            :class:`None`
        """
        super().__init__()

    @Command.register(name="/start", description="start something to the server \n /!\\ This is a parent command which permit to use other subcommand by passing her")
    async def execute(self, interaction: nextcord.Interaction, *args, **kwargs):
        """ # Start command execute method
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the Start command
        
        Access :
        ---
            src.bots.server_manager.bot_commands.Start.py\n
            Start.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Interaction of the command
        
        Returns :
        ---
            :class:`None`
        """
        pass