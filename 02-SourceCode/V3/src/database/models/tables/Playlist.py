from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table

from typing import Union

class Playlist(Table):
    """ # Playlist class
        
    Description :
    ---
        Manage database Playlists to use database with some specific function to retrieve some datas

    Access : 
    ---
        src.database.models.tables.Playlist.py\n
        Playlist

    inheritance : 
    ---
        - Table : :class:`Table` => Parent class of database tables
    """
    id = None               # Id of the playlist
    name = None             # Name of the playlist
    description = None      # Description of the playlist
    fk_file = None          # Foreign key of a file
    fk_server = None        # Foreign key of server

    TABLE = "playlist"      # Name of the table

    def __init__(self, id: int, name: str, description: str, fk_file: int, fk_server: int):
        """ # Class constructor of Playlist object 
        
        Description :
        ---
            Construct a Playlist object with parameters passed to use it more easily
        
        Access : 
        ---
            src.database.models.tables.Playlist.py\n
            Playlist.__init__()

        Parameters : 
        ---
            - id : :class:`int` => Id of the Playlist
            - name : :class:`str` => Name of the Playlist
            - description : :class:`str` => Description of the Playlist
            - fk_file : :class:`int` => Foreign key of file
            - fk_server : :class:`int` => Foreign key of server

        Returns : 
        ---
            :class:`None`
        """
        self.name = name
        self.description = description
        self.fk_file = fk_file
        self.fk_server = fk_server

        super().__init__(id)

    @staticmethod
    async def get_all_playlists() -> dict[bool, Union[list["Playlist"], str]]:
        """ # Get all Playlist function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get all the Playlists stored in the database table
        
        Access : 
        ---
            src.database.models.tables.Playlist.py\n
            Playlist.get_all_playlists()

        Returns : 
        ---
            :class:`list[Playlist]` => List of Playlists
        """
        # Get the query string
        query = f"SELECT * FROM {Playlist.TABLE};"

        # Execute the query
        result = await Database.get_instance().simple_exec(query)

        # Check if the query passed
        if result.get("passed"):
            return Playlist.format_list_object(result.get("cursor"), Playlist.create_object)
        else:
            return result
        
    @staticmethod
    async def get_playlist_by_id(id_playlist: int) -> dict[bool, Union["Playlist", str]]:
        """ # Get a Playlist by id function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get one Playlist stored in the database table by its id
        
        Access : 
        ---
            src.database.models.tables.Playlist.py\n
            Playlist.get_playlist_by_id()

        Parameters : 
        ---
            - id_Playlist : :class:`int` => Searched Playlist id

        Returns : 
        ---
            :class:`Playlist` => The Playlist which was got in database
        """
        # Get the query string
        where = "id_playlist = %(id_playlist)s"
        query = f"SELECT * FROM {Playlist.TABLE} WHERE {where};"
        
        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"id_playlist" : id_playlist})

        # Check if the query passed
        if result.get("passed"):
            return Playlist.format_object(result.get("cursor"), Playlist.create_object)
        else:
            return result
        
    @staticmethod
    async def get_playlist_by_name(name: str) -> dict[bool, Union["Playlist", str]]:
        """ # Get a Playlist by name function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get one Playlist stored in the database table by its name
        
        Access : 
        ---
            src.database.models.tables.Playlist.py\n
            Playlist.get_playlist_by_name()

        Parameters : 
        ---
            - name : :class:`str` => Searched Playlist name

        Returns : 
        ---
            :class:`Playlist|None` => The Playlist which was got in database
        """
        # Get the query string
        where = "name = %(name)s"
        query = f"SELECT * FROM {Playlist.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"name" : name})

        # Check if the query passed
        if result.get("passed"):
            return Playlist.format_object(result.get("cursor"), Playlist.create_object)
        else:
            return result
        
    @staticmethod
    def create_object(row: list) -> "Playlist":
        """ # Create object function
        @staticmethod
        
        Description :
        ---
            Create a :class:`Playlist` object by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.Playlist.py\n
            Playlist.create_object()

        Parameters : 
        ---
            - row : :class:`list` => Row of the result

        Returns : 
        ---
            :class:`Playlist` => A Playlist object
        """
        # Get the datas from the row
        id = row.get("id_playlist") if "id_playlist" in row else None
        name = row.get("name") if "name" in row else None
        description = row.get("description") if "description" in row else None
        fk_file = row.get("fk_file") if "fk_file" in row else None
        fk_server = row.get("fk_server") if "fk_server" in row else None

        # Create a Playlist object and return it
        return Playlist(id=id, name=name, description=description, fk_file=fk_file, fk_server=fk_server)