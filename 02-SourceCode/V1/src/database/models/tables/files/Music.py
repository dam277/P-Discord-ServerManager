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
    
    @staticmethod
    async def add_file(name: str, path: str, fk_server: int):
        """ # Add file Music function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Add a Music to the database table
            Override the parent function to add a file to the database
        
        Access : 
        ---
            src.database.models.tables.files.Music.py\n
            Music.add_file()

        Parameters : 
        ---
            - name : :class:`str` => Name of the Music
            - path : :class:`str` => Path to the Music
            - fk_server : :class:`int` => Foreign key of the server id

        Returns : 
        ---
            :class:`None`
        """
        message = await File.add_file(name, path, fk_server)
        
        # Get the query string
        fields = "(id_file)"
        params = "(%(id_file)s)"
        query = f"INSERT INTO {Music.TABLE} {fields} VALUES {params};"

        # Execute the query with the values
        result = await Database.get_instance().bind_exec(query, {"id_file": await Music.get_last_file_id()})
        if result[1] is False:
            return result[0]
        
        # Return the message
        return message.replace("file", "music")
    