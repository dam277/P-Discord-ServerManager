import nextcord

from .....database.models.srvm_tables.files.Music import Music

from ...._commands.Command import Command
from ..Get import Get

from ...srvm_views.PlaylistView import PlaylistView

from .....database.models.srvm_tables.Playlist import Playlist
from .....database.models.srvm_tables.Server import Server

class GetPlaylist(Get):
    """ # GetPlaylist command class
    
    Description :
    ---
        Manage the GetPlaylist command discord command
    
    Access :
    ---
        src.bots.server_manager.srvm_commands.notes.GetPlaylist.py\n
        GetPlaylist
    
    inheritance :
    ---
        - Command : :class:`Command` => Parent class of database commands
    """
    def __init__(self, playlist_name: str, guild_id: int):
        """ # GetPlaylist command constructor

        Description :
        ---
            Construct a GetPlaylist command object
        
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.GetPlaylist.py\n
            GetPlaylist.__init__()
        
        Parameters :
        ---
            - playlist_name : :class:`str` => Name of the playlist
            - guild_id : :class:`int` => Guild id of the playlist
        
        Returns :
        ---
            :class:`None`
        """
        self.playlist_name = playlist_name
        self.guild_id = guild_id

        super().__init__()

    @Command.register(name="get_playlist", description="Get a playlist from the discord server", parent="/get", playlist_name="Name of the playlist")
    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute command function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the command and make all connections with models and frontend (discord chat)
        
        Access :
        ---
            src.bots.server_manager.srvm_commands.notes.GetPlaylist.py\n
            GetPlaylist.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Discord interaction object
        
        Returns :
        ---
            :class:`None`
        """

               # Execute the parent function
        # Execute the parent command
        await super().execute(interaction)
        if not self.has_permission:
            return
        
        # Get the server id
        server_id_result = await Server.get_server_id_by_guild_id(self.guild_id)

        # Check if the server exists
        if not server_id_result.get("value") or not server_id_result.get("passed"):
            return await interaction.send(f"This server is not registered in the database, use /setup first", ephemeral=True) if server_id_result.get("error") is None else await interaction.send(f"An error occured while getting the server id : {server_id_result.get("error")}", ephemeral=True)
        
        # Get the playlist 
        playlist_result = await Playlist.get_playlist_by_name_and_fk_server(self.playlist_name, server_id_result.get("value"))
        playlist = playlist_result.get("object")

        # Check if the playlist exists
        if not playlist or not playlist_result.get("passed"):
            return await interaction.send(f"This playlist doesn't exist", ephemeral=True) if playlist_result.get("error") is None else await interaction.send(f"An error occured while getting the playlist : {playlist_result.get("error")}", ephemeral=True)
        
        # Get the associated musics
        musics_id_result = await Music.get_musics_by_playlist_id(playlist.id)
        musics = musics_id_result.get("objects")

        # Check if the notes exists
        if not musics or not musics_id_result.get("passed"):
            return await interaction.send(f"This playlist **{playlist.name}** doesn't have any music", ephemeral=True) if musics_id_result.get("error") is None else await interaction.send(f"An error occured while getting the music : {musics_id_result.get("error")}", ephemeral=True)

        # Create the embed
        playlist_embed = nextcord.Embed(title=playlist.name)
        playlist_embed.set_footer(text=f"Music 1/{len(musics)}")

        # Create the playlist view
        playlist_view = PlaylistView(musics, playlist_embed)
        await playlist_view.execute(interaction)

        return await interaction.send(embed=playlist_embed, view=playlist_view)

        # pages = []
        # # Create a list of list of dictionaries with music
        # for i in range(0, len(notes), 5):
        #     pages.append([{"title": note.title, "text": note.text} for note in notes[i:i + 5]])

        # # Make the notelist as embed
        # playlist_embed = nextcord.Embed(title=playlist.name)

        # # Page view for the embed
        # page_view = PageView(pages, playlist_embed)
        # await page_view.execute(interaction)

        # # Check if the playlist has an image
        # if playlist.fk_file:
        #     # Get the file
        #     file_result = await File.get_file_by_id(playlist.fk_file)

        #     # Check if the file exists
        #     if file_result.get("object"):
        #         file = nextcord.File(file_result.get("object").path, filename='thumbnail.png')  
        #         playlist_embed.set_thumbnail(url='attachment://thumbnail.png')

        #     # Send the embed with the image
        #     return await interaction.send(file=file, embed=playlist_embed, view=page_view)

        # # Send the embed without the image
        # return await interaction.send(embed=playlist_embed, view=page_view)