import nextcord
from nextcord.ext import commands
import os

from ....utils.enums.permissions.DiscordPermissions import DiscordPermissions

from ..._commands.Command import Command

class Delete(Command):
    """ # Delete command 
    
    Description :
    ---
        Delete a file to the server
    
    Access :
    ---
        src.bots.server_manager.bot_commands.Delete.py\n
        Delete
    
    Inheritence :
    ---
        :class:`Command`
    """

    def __init__(self):
        """ # Delete command constructor

        Description :
        ---
            Construct a Delete command object
        
        Access : 
        ---
            src.bots.server_manager.bot_commands.Delete.py\n
            Delete.__init__()

        Parameters :
        ---
            - guild_id : :class:`int` => Guild id of the command
            - file : :class:`nextcord.Attachment` => File to Delete

        Returns : 
        ---
            :class:`None`
        """
        super().__init__()

    #@Command.permissions([DiscordPermissions.administrator])
    @Command.register(name="/delete", description="Delete something to the server \n /!\\ This is a parent command which permit to use other subcommand by passing her")
    async def execute(self, interaction: nextcord.Interaction, *args, **kwargs):
        """ # Delete command execute method
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the Delete command
        
        Access :
        ---
            src.bots.server_manager.bot_commands.Delete.py\n
            Delete.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Interaction of the command
        
        Returns :
        ---
            :class:`None`
        """
        pass