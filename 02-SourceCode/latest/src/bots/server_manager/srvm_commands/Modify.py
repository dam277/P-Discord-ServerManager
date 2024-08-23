import nextcord
from nextcord.ext import commands
import os

from ....utils.enums.permissions.DiscordPermissions import DiscordPermissions

from ..._commands.Command import Command

class Modify(Command):
    """ # Modify command 
    
    Description :
    ---
        Modify a file to the server
    
    Access :
    ---
        src.bots.server_manager.bot_commands.Modify.py\n
        Modify
    
    Inheritence :
    ---
        :class:`Command`
    """

    def __init__(self):
        """ # Modify command constructor

        Description :
        ---
            Construct a Modify command object
        
        Access : 
        ---
            src.bots.server_manager.bot_commands.Modify.py\n
            Modify.__init__()

        Parameters :
        ---
            - guild_id : :class:`int` => Guild id of the command
            - file : :class:`nextcord.Attachment` => File to Modify

        Returns : 
        ---
            :class:`None`
        """
        super().__init__()

    #@Command.permissions([DiscordPermissions.administrator])
    @Command.register(name="/modify", description="Modify something to the server \n /!\\ This is a parent command which permit to use other subcommand by passing her")
    async def execute(self, interaction: nextcord.Interaction, *args, **kwargs):
        """ # Modify command execute method
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the Modify command
        
        Access :
        ---
            src.bots.server_manager.bot_commands.Modify.py\n
            Modify.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Interaction of the command
        
        Returns :
        ---
            :class:`None`
        """
        pass