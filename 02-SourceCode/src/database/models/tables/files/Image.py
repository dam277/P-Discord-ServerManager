from mysql.connector.cursor import MySQLCursor
from ....Database import Database
from ..File import File

class Image(File):
    """ # Image class
        
    Description :
    ---
        Manage database images to use database with some specific function to retrieve some datas

    Access : 
    ---
        src.database.models.tables.files.image.py\n
        Image

    inheritance : 
    ---
        - File : :class:`File` => Parent class of database Files
    """
    TABLE = "image"          # Database table name

    def __init__(self, id: int|None, name: str|None, path: str|None, fk_server: int|None):
        """ # Class constructor of Image object 
        
        Description :
        ---
            Construct a Image object with parameters passed to use it more easily
        
        Access : 
        ---
            src.database.models.tables.files.Image.py\n
            Image.__init__()

        Parameters : 
        ---
            - id : :class:`int` => Id of the Image
            - name : :class:`str` => Name of the Image
            - path : :class:`str` => Path to the Image
            - fk_server : :class:`int` => Foreign key of the server id

        Returns : 
        ---
            :class:`None`
        """
        super().__init__(id, name, path, fk_server)

    @staticmethod
    async def get_all_images():
        """ # Get all Image function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get all the Images stored in the database table
        
        Access : 
        ---
            src.database.models.tables.files.image.py\n
            Image.get_all_Images()

        Returns : 
        ---
            :class:`list[File]` => List of Images
        """
        # Get the query string
        query = f"SELECT * FROM {Image.TABLE};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().simple_exec(query)
        return Image.format_list_object(cursor_result)

    @staticmethod
    async def add_file(name: str, path: str, fk_server: int):
        """ # Add file Image function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Add an Image to the database table
            Override the parent function to add a file to the database
        
        Access : 
        ---
            src.database.models.tables.files.image.py\n
            Image.add_file()

        Parameters : 
        ---
            - name : :class:`str` => Name of the Image
            - path : :class:`str` => Path to the Image
            - fk_server : :class:`int` => Foreign key of the server id

        Returns : 
        ---
            :class:`None`
        """
        message = await File.add_file(name, path, fk_server)
        
        # Get the query string
        fields = "(id_file)"
        params = "(%(id_file)s)"
        query = f"INSERT INTO {Image.TABLE} {fields} VALUES {params};"

        # Execute the query with the values
        result = await Database.get_instance().bind_exec(query, {"id_file": await Image.get_last_file_id()})
        if result[1] is False:
            return result[0]

        # Return the message
        return message.replace("file", "image")    