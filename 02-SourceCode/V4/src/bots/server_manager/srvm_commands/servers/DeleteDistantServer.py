from hmac import new
from re import A
import nextcord

from ..Delete import Delete
from ...._commands.Command import Command

from .....database.models.srvm_tables.NoteList import NoteList
from .....database.models.srvm_tables.Note import Note
from .....database.models.srvm_tables.Server import Server
from .....database.models.srvm_tables.DistantServer import DistantServer

from .....utils.enums.permissions.DiscordPermissions import DiscordPermissions

from .....utils.logger.Logger import Logger, LogDefinitions

class DeleteDistantServer(Delete):
    """ # DeleteDistantServer command class
    
    Description :
    ---
        Manage the DeleteDistantServer command discord command
    
    Access :
    ---
        src.bots.server_manager.srvm_commands.notes.DeleteDistantServer.py\n
        DeleteDistantServer
    
    inheritance :
    ---
        - Command : :class:`Command` => Parent class of database commands
    """
    def __init__(self, adress_port: str, guild_id: int):
        """ # DeleteDistantServer command constructor
        
        Description :
        ---
            Construct a DeleteDistantServer command object
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.DeleteDistantServer.py\n
            DeleteDistantServer.__init__()
        
        Parameters :
        ---
            - title : :class:`str` => Title of the note
            - text : :class:`str` => Text of the note
            - note_list_name : :class:`str` => Name of the note list
            
        Returns :
        ---
            :class:`None`
        """
        self.adress = adress_port.split(":")[0]
        self.port = adress_port.split(":")[1]
        self.guild_id = guild_id

        super().__init__()

    @Command.permissions([DiscordPermissions.administrator])
    @Command.register(name="delete_distant_server", description="Delete a distant server from the server", parent="/delete", adress_port="Adress and port of the server")
    async def execute(self, interaction: nextcord.Interaction):
        """ # DeleteDistantServer command execute method
        
        Description :
        ---
            Execute the DeleteDistantServer command
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.DeleteDistantServer.py\n
            DeleteDistantServer.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Discord interaction with the command
            
        Returns :
        ---
            :class:`None`
        """
        # Execute the parent function
        await super().execute(interaction)
        if not self.has_permission:
            return     
        
        # Get the server id
        server_id_result = await Server.get_server_id_by_guild_id(self.guild_id)

        # Check if the server exists
        if not server_id_result.get("value") or not server_id_result.get("passed"):
            return await interaction.send(f"This server is not registered in the database, use /setup first", ephemeral=True) if server_id_result.get("error") is None else await interaction.send(f"An error occured while getting the server id : {server_id_result.get("error")}", ephemeral=True)

        # Get the distant server
        distant_servers_result = await DistantServer.delete_distant_server_by_server_id_and_distant_server(server_id_result.get("value"), self.adress, self.port)

        await interaction.send("The distant server has been deleted")
        
            