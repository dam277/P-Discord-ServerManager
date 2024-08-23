import nextcord

from .....database.models.tables.Server import Server
from ....commands.Command import Command


class Setup(Command):
    """ # Setup command class 
        
    Description :
    ---
        Manage the setup discord command 

    Access : 
    ---
        src.bots.server_manager.bot_commands.setup.Setup.py\n
        Setup

    inheritance : 
    ---
        - Command : :class:`Command` => Parent class of database commands
    """
    def __init__(self, guild_id: int, name: str):
        """ # Setup command constructor

        Description :
        ---
            Construct a setup command object
        
        Access : 
        ---
            src.bots.server_manager.bot_commands.setup.Setup.py\n
            Setup.__init_()

        Parameters : 
        ---
            - guild_id : :class:`int` => id of the guild
            - name : :class:`str` => name of the guild

        Returns : 
        ---
            :class:`None`
        """
        self.guild_id = guild_id
        self.name = name
        super().__init__()

    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute command function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the command and make all connections with models and frontend (discord chat)
        
        Access : 
        ---
            src.bots.server_manager.bot_commands.setup.Setup.py\n
            Setup.execute()

        Parameters : 
        ---
            - interaction: :class:`nextcord.Interaction` => Interaction within the user and the command

        Returns : 
        ---
            :class:`None`
        """
        message = await Server.create_server(guild_id=self.guild_id, name=self.name)
        await interaction.response.send_message(message, ephemeral=True)
