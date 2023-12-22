from mysql.connector.cursor import MySQLCursor
from ....Database import Database
from ..File import File

class Music(File):
    TABLE = "music"          # Database table name

    def __init__(self, id: int|None, name: str|None, path: str|None, fk_server: int|None):
        """ Class constructor of a music object 
        $param id: int => Id of the music
        $param name: str => Name of the music
        $param path: str => Path to the music
        $param fk_server: int => Foreign key of the server id"""
        super().__init__(id, name, path, fk_server)

    @staticmethod
    async def get_all_musics():
        """ Get all the musics of the database """

        # Get the query string
        query = f"SELECT * FROM {Music.TABLE};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().simple_exec(query)
        return Music.format_list_object(cursor_result)
    