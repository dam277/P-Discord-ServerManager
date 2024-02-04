import nextcord
from nextcord.ext import commands
import os

from ....utils.enums.permissions.DiscordPermissions import DiscordPermissions

from ..._commands.Command import Command

class Create(Command):
    """ # Create command 
    
    Description :
    ---
        Create a file to the server
    
    Access :
    ---
        src.bots.server_manager.bot_commands.Create.py\n
        Create
    
    Inheritence :
    ---
        :class:`Command`
    """

    def __init__(self):
        """ # Create command constructor

        Description :
        ---
            Construct a Create command object
        
        Access : 
        ---
            src.bots.server_manager.bot_commands.Create.py\n
            Create.__init__()

        Parameters :
        ---
            - guild_id : :class:`int` => Guild id of the command
            - file : :class:`nextcord.Attachment` => File to Create

        Returns : 
        ---
            :class:`None`
        """
        super().__init__()

    #@Command.permissions([DiscordPermissions.administrator])
    @Command.register(name="/create", description="Create something to the server \n /!\\ This is a parent command which permit to use other subcommand by passing her")
    async def execute(self, interaction: nextcord.Interaction, *args, **kwargs):
        """ # Create command execute method
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the Create command
        
        Access :
        ---
            src.bots.server_manager.bot_commands.Create.py\n
            Create.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Interaction of the command
        
        Returns :
        ---
            :class:`None`
        """
        pass