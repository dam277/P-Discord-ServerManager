from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table

class File(Table):
    id = None               # Id of the file
    name = None             # Name of the file
    path = None             # Path to the file
    fk_server = None        # Foreign key of the server id

    TABLE = "file"          # Database table name

    def __init__(self, id: int|None, name: str|None, path: str|None, fk_server: int|None):
        """ Class constructor of a File object 
        $param id: int => Id of the file
        $param name: str => Name of the file
        $param path: str => Path to the file
        $param fk_server: int => Foreign key of the server id"""
        self.id = id
        self.name = name
        self.path = path
        self.fk_server = fk_server

    @staticmethod
    async def get_all_files():
        """ Get all the files of the database """

        # Get the query string
        query = f"SELECT * FROM {File.TABLE};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().simple_exec(query)
        return File.format_list_object(cursor_result)
    
    @staticmethod
    async def get_file_by_id(id_file: int):
        """ Get a file by id 
        $param id_file: int -> file id"""

        # Get the query string
        where = "id_file = %(id_file)s"
        query = f"SELECT * FROM {File.TABLE} WHERE {where};"
        
        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"id_file": id_file})
        return File.format_object(cursor_result)
    
    @staticmethod
    async def get_file_by_name(name: str):
        """ Get a file by name 
        $param name: str -> file name"""

        # Get the query string
        where = "name = %(name)s"
        query = f"SELECT * FROM {File.TABLE} WHERE {where};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"name": name})
        return File.format_object(cursor_result)


    @staticmethod
    async def add_file(name: str, path: str, fk_server: int) -> str:
        """ Add a file to the database 
        $param name: str -> name of the file
        $param path: str -> path of the file
        $param fk_server: int -> foreign key of the server
        Return message: str -> Message to send to the server"""
        
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
        """ Get a file by its path
        $param path: str -> file path
        Return File"""

        # Get the query string
        where = "path = %(path)s"
        query = f"SELECT * FROM {File.TABLE} WHERE {where};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"path": path})
        return File.format_object(cursor_result)
    
    @staticmethod
    async def get_files_by_server_id(id_server: int):
        """ Get files by the the server id
        $param id_server: int -> server id
        Return list[File]"""
         
        where = "file.fk_server = %(fk_server)s"
        query = f"SELECT * FROM {File.TABLE} WHERE {where};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"fk_server": id_server})
        
        return File.format_list_object(cursor_result)

    # FORMAT OBJECTS ----------------------------------------------------------------

    @staticmethod
    def format_object(cursor_result: MySQLCursor):
        """ Format a database result into a object 
        $param cursor_result: MySQLCursor -> result of the query 
        Return None | file -> None for no data, file for successfully getting data """
        # Getting datas from result
        row = Table.get_one_row(cursor_result[0])

        # Check if datas are filled
        if row is None or len(row) < 1:
            return None
        
        # Create a file object and return it
        file = File(id=row[0], name=row[1], path=row[2], fk_server=row[3])
        return file
    
    @staticmethod
    def format_list_object(cursor_result: MySQLCursor) -> list:
        """ Format a database result into a object 
        $param cursor_result: MySQLCursor -> result of the query 
        Return None | list[file] -> None for no data, list of files for successfully getting datas """
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