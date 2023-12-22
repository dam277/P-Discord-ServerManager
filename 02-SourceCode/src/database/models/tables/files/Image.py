from mysql.connector.cursor import MySQLCursor
from ....Database import Database
from ..File import File

class Image(File):
    TABLE = "image"          # Database table name

    def __init__(self, id: int|None, name: str|None, path: str|None, fk_server: int|None):
        """ Class constructor of a image object 
        $param id: int => Id of the image
        $param name: str => Name of the image
        $param path: str => Path to the image
        $param fk_server: int => Foreign key of the server id"""
        super().__init__(id, name, path, fk_server)

    @staticmethod
    async def get_all_images():
        """ Get all the images of the database """

        # Get the query string
        query = f"SELECT * FROM {Image.TABLE};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().simple_exec(query)
        return Image.format_list_object(cursor_result)
    