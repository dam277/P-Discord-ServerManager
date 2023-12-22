from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table

class Playlist(Table):
    id = None               # Id of the playlist
    name = None             # Name of the playlist
    description = None      # Description of the playlist
    fk_file = None          # Foreign key of a file
    fk_server = None        # Foreign key of server

    TABLE = "playlist"      # Name of the table

    def __init__(self, id: int|None, name: str|None, description: str|None, fk_file: int|None, fk_server: int|None):
        """ Class constructor of a Playlist object 
        $param id: int => Id of the Playlist
        $param name: str => Name of the Playlist
        $param description: str => Description of the Playlist
        $param fk_file: int => Foreign key of file
        $param fk_server: int => Foreign key of server"""
        self.id = id
        self.name = name
        self.description = description
        self.fk_file = fk_file
        self.fk_server = fk_server

    @staticmethod
    async def get_all_playlist():
        """ Get all the playlists of the database """

        # Get the query string
        query = f"SELECT * FROM {Playlist.TABLE};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().simple_exec(query)
        return Playlist.format_list_object(cursor_result)
    
    @staticmethod
    async def get_playlist_by_id(id_playlist: int):
        """ Get a playlist by id 
        $param id_playlist: int -> note id"""

        # Get the query string
        where = "id_playlist = %(id_playlist)s"
        query = f"SELECT * FROM {Playlist.TABLE} WHERE {where};"
        
        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"id_playlist": id_playlist})
        return Playlist.format_object(cursor_result)
    
    @staticmethod
    async def get_playlist_by_name(name: str):
        """ Get a playlist by name 
        $param name: str -> playlist name"""

        # Get the query string
        where = "name = %(name)s"
        query = f"SELECT * FROM {Playlist.TABLE} WHERE {where};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"name": name})
        return Playlist.format_object(cursor_result)
    
    # FORMAT OBJECTS ----------------------------------------------------------------

    @staticmethod
    def format_object(cursor_result: MySQLCursor):
        """ Format a database result into a object 
        $param cursor_result: MySQLCursor -> result of the query 
        Return None | Playlist -> None for no data, Playlist for successfully getting data """

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
        """ Format a database result into a object 
        $param cursor_result: MySQLCursor -> result of the query 
        Return None | list[Playlist] -> None for no data, list of Playlists for successfully getting datas """
        
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