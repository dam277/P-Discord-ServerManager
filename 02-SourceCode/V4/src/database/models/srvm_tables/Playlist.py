from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table

from ....utils.enums.Databases import Databases

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
    DATABASE = Databases.server_manager # Database of the server table

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
        result = await Database.get_instance(Playlist.DATABASE).simple_exec(query)

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
        result = await Database.get_instance(Playlist.DATABASE).bind_exec(query, {"id_playlist" : id_playlist})

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
        result = await Database.get_instance(Playlist.DATABASE).bind_exec(query, {"name" : name})

        # Check if the query passed
        if result.get("passed"):
            return Playlist.format_object(result.get("cursor"), Playlist.create_object)
        else:
            return result
        
    @staticmethod
    async def get_playlists_by_server_id(id_server: int) -> dict[bool, Union[list["Playlist"], str]]:
        """ # Get Playlist by server id function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get a list of Playlists using the server id
        
        Access : 
        ---
            src.database.models.tables.Playlist.py\n
            Playlist.get_Playlists_by_server_id()

        Parameters : 
        ---
            - id_server : :class:`int` => Searched server id

        Returns : 
        ---
            :class:`list[Playlist]` => A list of Playlists got
        """
        where = "fk_server = %(fk_server)s"
        query = f"SELECT * FROM {Playlist.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance(Playlist.DATABASE).bind_exec(query, {"fk_server" : id_server})

        # Check if the query passed
        if result.get("passed"):
            return Playlist.format_list_object(result.get("cursor"), Playlist.create_object)
        else:
            return result
        
    @staticmethod
    async def get_playlist_id_by_name_and_fk_server(name: str, fk_server: int) -> dict[bool, Union[int, str]]:
        """ # Get a playlist id by name and fk server function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get one playlist stored in the database table by its name
        
        Access : 
        ---
            src.database.models.tables.NoteList.py\n
            NoteList.get_playlist_id_by_name_and_fk_server()

        Parameters : 
        ---
            - name : :class:`str` => Searched playlist name

        Returns : 
        ---
            :class:`int` => the note id
        """
        # Get the query string
        where = "fk_server = %(fk_server)s AND name = %(name)s"
        query = f"SELECT id_playlist FROM {Playlist.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance(Playlist.DATABASE).bind_exec(query, {"name" : name, "fk_server" : fk_server})

        # Check if the query passed
        if result.get("passed"):
            return Playlist.format_object(result.get("cursor"), Playlist.create_object, True)
        else:
            return result
        
    @staticmethod
    async def get_playlist_by_name_and_fk_server(name: str, fk_server: int) ->  dict[bool, Union["Playlist", str]]:
        """ # Get a playlist by name and fk server function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get one playlist stored in the database table by its name and fk server
        
        Access : 
        ---
            src.database.models.tables.NoteList.py\n
            NoteList.get_playlist_by_name()

        Parameters : 
        ---
            - name : :class:`str` => Searched playlist name

        Returns : 
        ---
            :class:`int` => the note id
        """
        # Get the query string
        where = "fk_server = %(fk_server)s AND name = %(name)s"
        query = f"SELECT * FROM {Playlist.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance(Playlist.DATABASE).bind_exec(query, {"name" : name, "fk_server" : fk_server})

        # Check if the query passed
        if result.get("passed"):
            return Playlist.format_object(result.get("cursor"), Playlist.create_object)
        else:
            return result
        
    @staticmethod
    async def create_playlist(name: str, description: str, id_file: int, id_server: int) -> dict[bool, Union[MySQLCursor, str]]:
        """ # Create a playlist function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Create a playlist in the database table
        
        Access : 
        ---
            src.database.models.tables.NoteList.py\n
            NoteList.create_playlist()

        Parameters : 
        ---
            - name : :class:`str` => Name of the playlist
            - fk_server : :class:`int` => Foreign key of the server id

        Returns : 
        ---
            :class:`NoteList|None` => The playlist which was created in database
        """
        # Get the query string
        fields = "(id_playlist, name, description, fk_file, fk_server)"
        params = "(null, %(name)s, %(description)s, %(fk_file)s, %(fk_server)s)"
        query = f"INSERT INTO {Playlist.TABLE} {fields} VALUES {params};"

        # Execute the query
        result = await Database.get_instance(Playlist.DATABASE).bind_exec(query, {"name" : name, "description" : description, "fk_file" : id_file, "fk_server" : id_server})

        # Return the result
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