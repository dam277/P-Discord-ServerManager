import nextcord

from ..Add import Add
from ...._commands.Command import Command
from .....utils.enums.FileTypes import FileTypes

from .....database.models.srvm_tables.Playlist import Playlist
from .....database.models.srvm_tables.sub_tables.MusicPlaylist import MusicPlaylist
from .....database.models.srvm_tables.Server import Server

class AddMusicToPlaylist(Add):
    """ # AddMusicToPlaylist command class
    
    Description :
    ---
        Manage the AddMusicToPlaylist command discord command
    
    Access :
    ---
        src.bots.server_manager.srvm_commands.notes.AddMusicToPlaylist.py\n
        AddMusicToPlaylist
    
    inheritance :
    ---
        - Command : :class:`Command` => Parent class of database commands
    """
    def __init__(self, file_name: str, playlist_name: str, guild_id: int):
        """ # AddMusicToPlaylist command constructor
        
        Description :
        ---
            Construct a AddMusicToPlaylist command object
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.AddMusicToPlaylist.py\n
            AddMusicToPlaylist.__init__()
        
        Parameters :
        ---
            - title : :class:`str` => Title of the note
            - text : :class:`str` => Text of the note
            - note_list_name : :class:`str` => Name of the music list
            
        Returns :
        ---
            :class:`None`
        """
        self.file_name = file_name
        self.playlist_name = playlist_name
        self.guild_id = guild_id

        super().__init__()

    @Command.register(name="add_music_to_playlist", description="Add a music to a playlist", parent="/add", file_name="Name of the music file to add into the playlist", playlist_name="Name of the playlist to add to")
    async def execute(self, interaction: nextcord.Interaction):
        """ # AddMusicToPlaylist command execute method
        
        Description :
        ---
            Execute the AddMusicToPlaylist command
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.AddMusicToPlaylist.py\n
            AddMusicToPlaylist.execute()
        
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
        
        # Get the playlist id
        playlist_id_result = await Playlist.get_playlist_id_by_name_and_fk_server(self.playlist_name, server_id_result.get("value"))
        
        # Check if the playlist exists
        if not playlist_id_result.get("value") or not playlist_id_result.get("passed"):
            return await interaction.send(f"the music list **{self.playlist_name}** does not exists, use **/create note_list** to add it", ephemeral=True) if playlist_id_result.get("error") is None else await interaction.send(f"An error occured while getting the music list id : {playlist_id_result.get("error")}", ephemeral=True)
        
        # Check if the file exists
        file_id = await self.get_file_id_by_type(interaction)
        
        # Check if the music exists in the playlist
        musics_id_result = await MusicPlaylist.get_musics_id_from_playlist_id(playlist_id_result.get("value"))

        if not musics_id_result.get("passed"):
            return await interaction.send(f"An error occured while getting the musics from the playlist : {musics_id_result.get("error")}", ephemeral=True)
        
        # Check if the music is already in the playlist
        if file_id in musics_id_result.get("values"):
            return await interaction.send(f"The music {self.file_name} is already in the playlist {self.playlist_name}", ephemeral=True)

        # Check if the file is a music
        self.get_file_type(self.file_name)
        if self.file_type != FileTypes.MUSIC:
            return await interaction.send(f"The file {self.file_name} is not a music file", ephemeral=True)

        # Add the music to the playlist
        result = await MusicPlaylist.add_music_to_playlist(file_id, playlist_id_result.get("value"))

        # Check if the music has been added
        if not result.get("passed"):
            return await interaction.send(f"An error occured while adding the music : {result.get("error")}", ephemeral=True)
        return await interaction.send(f"the music {self.file_name} has been added to the playlist {self.playlist_name}", ephemeral=True)