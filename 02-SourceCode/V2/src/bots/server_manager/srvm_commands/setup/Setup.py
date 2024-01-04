import nextcord

from ...._commands.Command import Command

from .....database.models.tables.Server import Server

from .....utils.logger.Logger import Logger, LogDefinitions

class Setup(Command):
    """ # Setup command

    Description :
    ---
        Create a server and save it in the database

    Access :
    ---
        src.bots.server_manager.bot_commands.setup.Setup.py\n
        Setup
    
    Inheritence :
    ---
        :class:`Command`
    
    """
    def __init__(self, guild_id: int, name: str):
        """ # Setup command constructor

        Description :
        ---
            Create a setup command instance

        Access :
        ---
            src.bots.server_manager.bot_commands.setup.Setup.py\n
            Setup.__init__()
        
        Parameters :
        ---
            - guild_id: :class:`int` => Id of the guild where the command is used
            - name: :class:`str` => Name of the server to create

        Returns :
        ---
            :class:`None`
        """
        self.guild_id = guild_id
        self.name = name
        super().__init__()

    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute function of the setup command

        Description :
        ---
            Create a server and save it in the database
        
        Access :
        ---
            src.bots.server_manager.bot_commands.setup.Setup.py\n
            Setup.execute()
        
        Parameters :
        ---
            - interaction: :class:`nextcord.Interaction` => The interaction of the command
        
        Returns :
        ---
            :class:`None`
        """
        Logger.log(LogDefinitions.INFO, f"{__class__.__name__} command executed in guild {interaction.user.name}")
        message = await Server.create_server(guild_id=self.guild_id, name=self.name)
        await interaction.response.send_message(message, ephemeral=True)

