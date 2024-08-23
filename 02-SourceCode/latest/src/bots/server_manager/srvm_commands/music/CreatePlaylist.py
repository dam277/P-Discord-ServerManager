import nextcord

from ..Create import Create
from ...._commands.Command import Command

from .....utils.enums.FileTypes import FileTypes

from .....database.models.srvm_tables.Playlist import Playlist
from .....database.models.srvm_tables.Server import Server

from .....utils.logger.Logger import Logger, LogDefinitions

class CreatePlaylist(Create):
    """ # CreateNoteList command class
    
    Description :
    ---
        Manage the CreateNoteList command discord command
    
    Access :
    ---
        src.bots.server_manager.srvm_commands.notes.CreateNoteList.py\n
        CreateNoteList
    
    inheritance :
    ---
        - Command : :class:`Command` => Parent class of database commands
    """
    def __init__(self, playlist_name: str, description: str, file_name: str|None, guild_id: int):
        """ # CreateNoteList command constructor
        
        Description :
        ---
            Construct a CreateNoteList command object
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.CreateNoteList.py\n
            CreateNoteList.__init__()
        
        Parameters :
        ---
            - playlist_name : :class:`str` => Name of the playlist
            - description : :class:`str` => Description of the playlist
            - file_name : :class:`str` => Name of the file to import into the playlist
            - guild_id : :class:`int` => Discord guild id
        
        Returns :
        ---
            :class:`None`
        """
        self.playlist_name = playlist_name
        self.description = description
        self.file_name = file_name
        self.guild_id = guild_id
        super().__init__()

    @Command.register(name="create_playlist", description="Create a playlist to play musics on a vocal channel", parent="/create", playlist_name="Name of the playlist", file_name="[optional]Name of the file to import into the playlist")
    async def execute(self, interaction: nextcord.Interaction):
        """ # CreateNoteList command execute method
        
        Description :
        ---
            Execute the CreateNoteList command
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.CreateNoteList.py\n
            CreateNoteList.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Discord interaction
            
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
        
        # Check if the file exists
        file_id = await self.get_file_id_by_type(interaction)
                
        # Check if the playlist already exists
        playlist_result = await Playlist.get_playlist_id_by_name_and_fk_server(self.playlist_name, server_id_result.get("value"))
        if playlist_result.get("object") is not None:
            return await interaction.send(f"This playlist already exists", ephemeral=True)
        
        # Check if the file exists
        if self.file_name:
            # Check if the file is an image
            self.get_file_type(self.file_name)
            if self.file_type != FileTypes.IMAGE:
                return await interaction.send(f"The file {self.file_name} is not an image file", ephemeral=True)
        
        # Create the playlist
        result = await Playlist.create_playlist(self.playlist_name, self.description, file_id, server_id_result.get("value"))

        # Check if the query passed
        if not result.get("passed"):
            Logger.log(LogDefinitions.ERROR, f"An error occured while creating the playlist : {result.get("error")}")
            return await interaction.send(f"An error occured while creating the playlist : {result.get("error")}", ephemeral=True)
        
        # Send the message
        await interaction.send(f"Playlist **{self.playlist_name}** created !")

