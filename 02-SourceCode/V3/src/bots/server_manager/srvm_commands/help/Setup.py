import nextcord
from nextcord.ext import commands

from .....utils.enums.permissions.DiscordPermissions import DiscordPermissions

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

    @Command.permissions([DiscordPermissions.manage_guild])
    @Command.register(name="/setup", description="Setup the server into the database to be able to use the bot with this discord server")
    async def execute(self, interaction: nextcord.Interaction):
        """ # Setup command execution

        Description :
        ---
            Create a server and save it in the database
        
        Access :
        ---
            src.bots.server_manager.bot_commands.setup.Setup.py\n
            Setup.setup()
        
        Parameters :
        ---
            - interaction: :class:`nextcord.Interaction` => The interaction of the command
        
        Returns :
        ---
            :class:`None`
        """
        # Check if the server already exists in the database
        srv_result = await Server.get_server_by_guild_id(guild_id=self.guild_id)
        if not srv_result.get("passed"):
            Logger.log(LogDefinitions.ERROR, f"Error while checking if server {self.name} already exists : {srv_result.get('error')}")
            return await interaction.send(f"Error while checking if server {self.name} already exists", ephemeral=True)

        # Check if the server already exists
        if srv_result.get("object") is None:
            # Create the server
            result = await Server.create_server(guild_id=self.guild_id, name=self.name)

            # Check if the query passed
            if result.get("passed"):
                return await interaction.send(f"Server {self.name} created", ephemeral=True)

        # If the server already exists return an error message as discord response
        return await interaction.send(f"Server {self.name} already exists", ephemeral=True)