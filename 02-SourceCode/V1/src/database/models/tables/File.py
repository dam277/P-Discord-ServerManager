from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table

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
        self.id = id
        self.name = name
        self.path = path
        self.fk_server = fk_server

    @staticmethod
    async def get_all_files() -> list["File"]:
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

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().simple_exec(query)
        return File.format_list_object(cursor_result)
    
    @staticmethod
    async def get_last_file_id() -> "File":
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
        query = f"SELECT * FROM {File.TABLE} WHERE id_file = (SELECT MAX(id_file) FROM file)"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().simple_exec(query)
        return File.format_object(cursor_result).id
    
    @staticmethod
    async def get_file_by_id(id_file: int):
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
        
        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"id_file": id_file})
        return File.format_object(cursor_result)
    
    @staticmethod
    async def get_file_by_name(name: str):
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

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"name": name})
        return File.format_object(cursor_result)


    @staticmethod
    async def add_file(name: str, path: str, fk_server: int) -> str:
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
        params = "(%(id_file)s, %(name)s, %(path)s, %(fk_server)s)"
        query = f"INSERT INTO {File.TABLE} {fields} VALUE {params};"

        # Get the server and define if it already exists
        obj_file = await File.get_file_by_path(path)
        if obj_file is not None:
            return f"The file **'{name}'** already exists on the database"
        
        # If the server doesn't exists, insert it into the database
        result = await Database.get_instance().bind_exec(query, {"id_file" : None, "name": name, "path": path, "fk_server": fk_server})
        if result[1] is True:
            message = f"The file **'{name}'** has been successfully added to the database"
        else:
            message = result

        # Return the message to the user
        return message
        
    @staticmethod
    async def get_file_by_path(path: str):
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

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"path": path})
        return File.format_object(cursor_result)
    
    @staticmethod
    async def get_files_by_server_id(id_server: int):
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

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"fk_server": id_server})

        return File.format_list_object(cursor_result)

    # FORMAT OBJECTS ----------------------------------------------------------------

    @staticmethod
    def format_object(cursor_result: MySQLCursor):
        """ # Format object function
        @staticmethod
        
        Description :
        ---
            Format a :class:`File` object by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.File.py\n
            File.format_object()

        Parameters : 
        ---
            - cursor_result : :class:`MySQLCursor` => Result of the query

        Returns : 
        ---
            :class:`File|None` => A file object
        """
        # Getting datas from result
        row = Table.get_one_row(cursor_result[0])

        # Check if datas are filled
        if row is None or len(row) < 1:
            return None
        
        # Create a file object and return it
        file = File(id=row[0], name=row[1], path=row[2], fk_server=row[3])
        return file
    
    @staticmethod
    def format_list_object(cursor_result: MySQLCursor) -> list["File"]:
        """ # Format list object function
        @staticmethod
        
        Description :
        ---
            Format a :class:`File` object list by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.File.py\n
            File.format_list_object()

        Parameters : 
        ---
            - cursor_result : :class:`MySQLCursor` => Result of the query

        Returns : 
        ---
            :class:`list[File]|None` => A list of file object
        """
        # Getting datas from result
        rows = Table.get_all_rows(cursor_result[0])
        
        # Check if datas are filled
        if len(rows) < 1:
            return None
        
        # List all the files
        files = []
        for row in rows:
            # Create a file object and add it to the files list
            file = File(id=row[0], name=row[1], path=row[2], fk_server=row[3])
            files.append(file)

        return files