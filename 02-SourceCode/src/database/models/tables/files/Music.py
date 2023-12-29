from mysql.connector.cursor import MySQLCursor
from ....Database import Database
from ..File import File

class Music(File):
    """ # Music class
        
    Description :
    ---
        Manage database musics to use database with some specific function to retrieve some datas

    Access : 
    ---
        src.database.models.tables.files.Music.py\n
        Music

    inheritance : 
    ---
        - File : :class:`File` => Parent class of database Files
    """
    TABLE = "music"          # Database table name

    def __init__(self, id: int|None, name: str|None, path: str|None, fk_server: int|None):
        """ # Class constructor of Music object 
        
        Description :
        ---
            Construct a Music object with parameters passed to use it more easily
        
        Access : 
        ---
            src.database.models.tables.files.Music.py\n
            Music.__init__()

        Parameters : 
        ---
            - id : :class:`int` => Id of the Music
            - name : :class:`str` => Name of the Music
            - path : :class:`str` => Path to the Music
            - fk_server : :class:`int` => Foreign key of the server id

        Returns : 
        ---
            :class:`None`
        """
        super().__init__(id, name, path, fk_server)

    @staticmethod
    async def get_all_musics():
        """ # Get all Music function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get all the musics stored in the database table
        
        Access : 
        ---
            src.database.models.tables.Music.py\n
            Music.get_all_musics()

        Returns : 
        ---
            :class:`list[File]` => List of musics
        """
        # Get the query string
        query = f"SELECT * FROM {Music.TABLE};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().simple_exec(query)
        return Music.format_list_object(cursor_result)
    