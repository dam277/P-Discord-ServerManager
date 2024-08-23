import nextcord

from ....utils.enums.permissions.DiscordPermissions import DiscordPermissions

from ..._commands.Command import Command

class Add(Command):
    """ # Add command 
    
    Description :
    ---
        Add a file to the server
    
    Access :
    ---
        src.bots.server_manager.bot_commands.Add.py\n
        Add
    
    Inheritence :
    ---
        :class:`Command`
    """

    def __init__(self):
        """ # Add command constructor

        Description :
        ---
            Construct a Add command object
        
        Access : 
        ---
            src.bots.server_manager.bot_commands.Add.py\n
            Add.__init__()

        Parameters :
        ---
            - guild_id : :class:`int` => Guild id of the command
            - file : :class:`nextcord.Attachment` => File to add

        Returns : 
        ---
            :class:`None`
        """
        super().__init__()

    @Command.register(name="/add", description="Add something to the server \n /!\\ This is a parent command which permit to use other subcommand by passing her")
    async def execute(self, interaction: nextcord.Interaction, *args, **kwargs):
        """ # Add command execute method
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the Add command
        
        Access :
        ---
            src.bots.server_manager.bot_commands.Add.py\n
            Add.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Interaction of the command
        
        Returns :
        ---
            :class:`None`
        """
        pass