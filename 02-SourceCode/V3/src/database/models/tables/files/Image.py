from mysql.connector.cursor import MySQLCursor
from ....Database import Database
from ..File import File

from typing import Union

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

    def __init__(self, id: int, name: str, path: str, fk_server: int):
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
    async def get_all_images() -> dict[bool, Union[list["Image"], str]]:
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
        inner_join_file = f"INNER JOIN file ON {Image.TABLE}.id_file = {File.TABLE}.id_file"
        query = f"SELECT * FROM {Image.TABLE} {inner_join_file};"

        # Execute the query
        result = await Database.get_instance().simple_exec(query)

        # Check if the query passed
        if result.get("passed"):
            return Image.format_list_object(result.get("cursor"), Image.create_object)
        else:
            return result

    @staticmethod
    async def add_file(name: str, path: str, fk_server: int)  -> dict[bool, Union[MySQLCursor, str]]:
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
        result = await File.add_file(name, path, fk_server)
        
        # Check if the query passed
        if result.get("passed"):
            # Get the query string
            fields = "(id_file)"
            params = "(%(id_file)s)"
            query = f"INSERT INTO {Image.TABLE} {fields} VALUES {params};"

            # Get the last file id
            file_id_result = await File.get_last_file_id()
            
            # Execute the query
            result = await Database.get_instance().bind_exec(query, {"id_file" : file_id_result.get("value")})

        # Return the result
        return result
    
    @staticmethod
    async def delete_file_by_id(id_file: int) -> dict[bool, Union[MySQLCursor, str]]:
        """ # Delete file Image function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Delete a file by its id
            
        Access :
        ---
            src.database.models.tables.File.py\n
            File.delete_file_by_id()
        
        Parameters :
        ---
            - id_file : :class:`int` => Searched file id
        
        Returns :
        ---
            :class:`str` => The message which will be sent to the user
        """
        # Get the query string
        where = "id_file = %(id_file)s"
        query = f"DELETE FROM {Image.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"id_file" : id_file})

        # Check if the query passed
        if result.get("passed"):
            return File.delete_file_by_id(id_file)
        else:
            return result

        
