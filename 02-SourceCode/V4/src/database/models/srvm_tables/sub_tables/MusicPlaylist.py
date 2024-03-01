from difflib import restore
from traceback import format_list
from typing import Union

from mysql.connector.cursor import MySQLCursor
from attr import fields
from ....Database import Database
from ...Table import Table
from .....utils.enums.Databases import Databases

class MusicPlaylist(Table):
    """ # MusicPlaylist class

    Description :
    ---
        This class is used to represent a music playlist in the database

    Access : 
    ---
        src.database.models.srvm_tables.MusicPlaylist 
        MusicPlaylist

    Inheritance :
    ---
        - Table : :class:`Table` => Parent class of database
    """
    id_file = None
    id_playlist = None

    TABLE = "music_playlist"
    DATABASE = Databases.server_manager # Database of the server table

    def __init__(self, id_file: int, id_playlist: int):
        """ # Constructor method
        
        Description :
        ---
            Initializes the attributes of the class

        Access :
        ---
            src.database.models.srvm_tables.MusicPlaylist
            MusicPlaylist.__init__()

        Parameters :
        ---
            - id : :class:`int` => The id of the music playlist
            - name : :class:`str` => The name of the music playlist
            - fk_server : :class:`int` => The id of the server

        Returns :
        ---
            :class:`None`
        """
        self.id_file = id_file
        self.id_playlist = id_playlist
        super().__init__()

    @staticmethod
    async def get_musics_id_from_playlist_id(id_playlist: int) -> dict[bool, Union[list[int], str]]:
        """ # Get musics from playlist id method

        Description :
        ---
            This method is used to get the musics from a playlist id

        Access :
        ---
            src.database.models.srvm_tables.MusicPlaylist
            MusicPlaylist.get_musics_from_playlist_id()

        Parameters :
        ---
            - id_playlist : :class:`int` => The id of the playlist

        Returns :
        ---
            :class:`list` => A list of musics from the playlist id
        """
        # Get the query
        where = "id_playlist = %(id_playlist)s"
        query = f"SELECT id_file FROM {MusicPlaylist.TABLE} WHERE {where};"

        # Get the result
        result = await Database.get_instance(MusicPlaylist.DATABASE).bind_exec(query, {"id_playlist": id_playlist})

        # Check if the query passed
        if result.get("passed"):
            return MusicPlaylist.format_list_object(result.get("cursor"), lambda: (), True, True)
        else:
            return result
        
    @staticmethod
    async def add_music_to_playlist(id_file: int, id_playlist: int) -> dict[bool, Union[MySQLCursor, str]]:
        """ # Add music to playlist method

        Description :
        ---
            This method is used to add a music to a playlist

        Access :
        ---
            src.database.models.srvm_tables.MusicPlaylist
            MusicPlaylist.add_music_to_playlist()

        Parameters :
        ---
            - id_file : :class:`int` => The id of the file
            - id_playlist : :class:`int` => The id of the playlist

        Returns :
        ---
            :class:`dict` => A dictionary containing the result of the query
        """
        # Get the query
        fields = "(id_file, id_playlist)"
        params = "(%(id_file)s, %(id_playlist)s)"
        query = f"INSERT INTO {MusicPlaylist.TABLE} {fields} VALUES {params};"

        # Get the result
        result = await Database.get_instance(MusicPlaylist.DATABASE).bind_exec(query, {"id_file": id_file, "id_playlist": id_playlist})

        # Return the result
        return result