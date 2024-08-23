from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table
from typing import Union

from ....utils.enums.Databases import Databases

class File(Table):
    """ # File class
        
    Description :
    ---
        Manage database files to use database with some specific function to retrieve some datas

    Access : 
    ---
        src.database.models.tables.File.py\n
        File

    inheritance : 
    ---
        - Table : :class:`Table` => Parent class of database tables
    """
    id = None               # Id of the file
    name = None             # Name of the file
    path = None             # Path to the file
    fk_server = None        # Foreign key of the server id

    TABLE = "file"          # Database table name
    DATABASE = Databases.server_manager # Database of the server table

    def __init__(self, id: int|None, name: str|None, path: str|None, fk_server: int|None):
        """ # Class constructor of File object 
        
        Description :
        ---
            Construct a file object with parameters passed to use it more easily
        
        Access : 
        ---
            src.database.models.tables.File.py\n
            File.__init__()

        Parameters : 
        ---
            - id : :class:`int` => Id of the file
            - name : :class:`str` => Name of the file
            - path : :class:`str` => Path to the file
            - fk_server : :class:`int` => Foreign key of the server id

        Returns : 
        ---
            :class:`None`
        """
        self.name = name
        self.path = path
        self.fk_server = fk_server

        super().__init__(id)

    @staticmethod
    async def get_all_files() -> dict[bool, Union[list["File"], str]]:
        """ # Get all file function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get all the files stored in the database table
        
        Access : 
        ---
            src.database.models.tables.File.py\n
            File.get_all_files()

        Returns : 
        ---
            :class:`list[File]` => List of files
        """
        # Get the query string
        query = f"SELECT * FROM {File.TABLE};"
        
        # Execute the query
        result = await Database.get_instance(File.DATABASE).simple_exec(query)

        # Check if the query passed
        if result.get("passed"):
            return File.format_list_object(result.get("cursor"), File.create_object)
        else:
            return result
        
    @staticmethod
    async def get_last_file_id() -> dict[bool, Union[int, str]]:
        """ # Get the last file id function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get the last id of the file table
            
        Access : 
        ---
            src.database.models.tables.File.py\n
            File.get_last_file_id()

        Returns : 
        ---
            :class:`int|None` => The last id of the file table, or None if no records exist
        """
        # Get the query string
        query = f"SELECT id_file FROM {File.TABLE} WHERE id_file = (SELECT MAX(id_file) FROM file)"

        # Execute the query
        result = await Database.get_instance(File.DATABASE).simple_exec(query)  

        # Check if the query passed
        if result.get("passed"):
            return File.format_object(result.get("cursor"), File.create_object, True)
        else:
            return result
        
    @staticmethod
    async def get_file_by_id(id_file: int) -> dict[bool, Union["File", str]]:
        """ # Get a file by id function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get one file stored in the database table by its id
        
        Access : 
        ---
            src.database.models.tables.File.py\n
            File.get_file_by_id()

        Parameters : 
        ---
            - id_file : :class:`int` => Searched file id

        Returns : 
        ---
            :class:`File|None` => The file which was got in database
        """
        # Get the query string
        where = "id_file = %(id_file)s"
        query = f"SELECT * FROM {File.TABLE} WHERE {where};"
        
        # Execute the query
        result = await Database.get_instance(File.DATABASE).bind_exec(query, {"id_file" : id_file})

        # Check if the query passed
        if result.get("passed"):
            return File.format_object(result.get("cursor"), File.create_object)
        else:
            return result
        
    @staticmethod
    async def get_file_by_name(name: str) -> dict[bool, Union["File", str]]:
        """ # Get a file by name function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get one file stored in the database table by its name
        
        Access : 
        ---
            src.database.models.tables.File.py\n
            File.get_file_by_name()

        Parameters : 
        ---
            - name : :class:`str` => Searched file name

        Returns : 
        ---
            :class:`File|None` => The file which was got in database
        """
        # Get the query string
        where = "name = %(name)s"
        query = f"SELECT * FROM {File.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance(File.DATABASE).bind_exec(query, {"name" : name})

        # Check if the query passed
        if result.get("passed"):
            return File.format_object(result.get("cursor"), File.create_object)
        else:
            return result
        
    @staticmethod
    async def get_file_by_name_and_guild_id(name: str, guild_id: int) -> dict[bool, Union["File", str]]:
        """ # Get a file by name and guild id function
        /!\\ This is a coroutine, it needs to be awaited

        Description :
        ---
            Get one file stored in the database table by its name and guild id
        
        Access :
        ---
            src.database.models.tables.File.py\n
            File.get_file_by_name_and_guild_id()

        Parameters :
        ---
            - name : :class:`str` => Searched file name
            - guild_id : :class:`int` => Searched guild id

        Returns :
        ---
            :class:`File|None` => The file which was got in database
        """
        # Get the query string
        inner_select_guild_id = "SELECT id_server FROM server WHERE guildID = %(guild_id)s"
        where = f"fk_server = ({inner_select_guild_id}) AND name = %(name)s"
        query = f"SELECT * FROM {File.TABLE} WHERE {where};"  

        # Execute the query
        result = await Database.get_instance(File.DATABASE).bind_exec(query, {"name" : name, "guild_id" : guild_id})

        # Check if the query passed
        if result.get("passed"):
            return File.format_object(result.get("cursor"), File.create_object)
        else:
            return result

    @staticmethod
    async def add_file(name: str, path: str, fk_server: int) -> dict[bool, Union[MySQLCursor, str]]:
        """ # Add file function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Add a new file into the database with the right server (guild) associated
        
        Access : 
        ---
            src.database.models.tables.File.py\n
            File.add_file()

        Parameters : 
        ---
            - name : :class:`str` => File name
            - path : :class:`str` => File path
            - fk_server : :class:`int` => Associated server foreign key

        Returns : 
        ---
            :class:`str` => The message which will be sent to the user
        """
        # Get the query string
        fields = "(id_file, name, path, fk_server)"
        params = "(null, %(name)s, %(path)s, %(fk_server)s)"
        query = f"INSERT INTO {File.TABLE} {fields} VALUE {params};"

        # Execute the query
        result = await Database.get_instance(File.DATABASE).bind_exec(query, {"name" : name, "path" : path, "fk_server" : fk_server})

        # Return the result
        return result
    
    @staticmethod
    async def get_file_by_path(path: str) -> dict[bool, Union["File", str]]:
        """ # Get file by path function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get a file by its path
        
        Access : 
        ---
            src.database.models.tables.File.py\n
            File.get_file_by_path()

        Parameters : 
        ---
            - path : :class:`str` => Searched file path 

        Returns : 
        ---
            :class:`File|None` => The file which was got in database
        """
        # Get the query string
        where = "path = %(path)s"
        query = f"SELECT * FROM {File.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance(File.DATABASE).bind_exec(query, {"path" : path})

        # Check if the query passed
        if result.get("passed"):
            return File.format_object(result.get("cursor"), File.create_object)
        else:
            return result
    
    @staticmethod
    async def get_files_by_server_id(id_server: int) -> dict[bool, Union[list["File"], str]]:
        """ # Get file by server id function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get a list of files using the server id
        
        Access : 
        ---
            src.database.models.tables.File.py\n
            File.get_files_by_server_id()

        Parameters : 
        ---
            - id_server : :class:`int` => Searched server id

        Returns : 
        ---
            :class:`list[File]` => A list of files got
        """
        where = "file.fk_server = %(fk_server)s"
        query = f"SELECT * FROM {File.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance(File.DATABASE).bind_exec(query, {"fk_server" : id_server})

        # Check if the query passed
        if result.get("passed"):
            return File.format_list_object(result.get("cursor"), File.create_object)
        else:
            return result
        
    @staticmethod
    async def delete_file_by_id(id_file: int) -> dict[bool, Union[MySQLCursor, str]]:
        """ # Delete file by id function
        /!\\ This is a coroutine, it needs to be awaited
        
        @staticmethod

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
        query = f"DELETE FROM {File.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance(File.DATABASE).bind_exec(query, {"id_file" : id_file})

        # Return the result
        return result

    @staticmethod
    def create_object(row: dict) -> "File":
        """ # Create object function
        @staticmethod
        
        Description :
        ---
            Create a :class:`File` object by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.File.py\n
            File.create_object()

        Parameters : 
        ---
            - row : :class:`list` => Row of the result

        Returns : 
        ---
            :class:`File` => A File object
        """
        # Create a file object and return it
        id = row.get("id_file") if "id_file" in row else None
        name = row.get("name") if "name" in row else None
        path = row.get("path") if "path" in row else None
        fk_server = row.get("fk_server") if "fk_server" in row else None

        return File(id=id, name=name, path=path, fk_server=fk_server)
