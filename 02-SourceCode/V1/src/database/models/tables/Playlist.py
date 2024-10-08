from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table

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

    def __init__(self, id: int|None, name: str|None, description: str|None, fk_file: int|None, fk_server: int|None):
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
        self.id = id
        self.name = name
        self.description = description
        self.fk_file = fk_file
        self.fk_server = fk_server

    @staticmethod
    async def get_all_playlists():
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

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().simple_exec(query)
        return Playlist.format_list_object(cursor_result)
    
    @staticmethod
    async def get_playlist_by_id(id_playlist: int):
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
            :class:`Playlist|None` => The Playlist which was got in database
        """
        # Get the query string
        where = "id_playlist = %(id_playlist)s"
        query = f"SELECT * FROM {Playlist.TABLE} WHERE {where};"
        
        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"id_playlist": id_playlist})
        return Playlist.format_object(cursor_result)
    
    @staticmethod
    async def get_playlist_by_name(name: str):
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

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"name": name})
        return Playlist.format_object(cursor_result)
    
    # FORMAT OBJECTS ----------------------------------------------------------------

    @staticmethod
    def format_object(cursor_result: MySQLCursor):
        """ # Format object function
        @staticmethod
        
        Description :
        ---
            Format a :class:`Playlist` object by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.Playlist.py\n
            Playlist.format_object()

        Parameters : 
        ---
            - cursor_result : :class:`MySQLCursor` => Result of the query

        Returns : 
        ---
            :class:`Playlist|None` => A Playlist object
        """
        # Getting datas from result
        row = Table.get_one_row(cursor_result[0])

        # Check if datas are filled
        if row is None or len(row) < 1:
            return None
        
        # Create a note object and return it
        playlist = Playlist(id=row[0], name=row[1], description=row[2], fk_file=row[3], fk_server=row[4])
        return playlist
    
    @staticmethod
    def format_list_object(cursor_result: MySQLCursor) -> list:
        """ # Format list object function
        @staticmethod
        
        Description :
        ---
            Format a :class:`Playlist` object list by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.Playlist.py\n
            Playlist.format_list_object()

        Parameters : 
        ---
            - cursor_result : :class:`MySQLCursor` => Result of the query

        Returns : 
        ---
            :class:`list[Playlist]|None` => A list of Playlist object
        """
        # Getting datas from result
        rows = Table.get_all_rows(cursor_result[0])

        # Check if datas are filled
        if len(rows) < 1:
            return None
        
        # List all the servers
        playlists = list
        for row in rows:
            # Create a server object and add it to the servers list
            playlist = Playlist(id=row[0], name=row[1], description=row[2], fk_file=row[3], fk_server=row[4])
            playlists.append(playlist)
        return playlists