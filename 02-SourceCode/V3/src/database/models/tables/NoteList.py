from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table
from typing import Union

class NoteList(Table):
    """ # NoteList class
        
    Description :
    ---
        Manage database note lists to use database with some specific function to retrieve some datas

    Access : 
    ---
        src.database.models.tables.NoteList.py\n
        NoteList

    inheritance : 
    ---
        - Table : :class:`Table` => Parent class of database tables
    """
    id = None               # Id of the note list
    name = None             # Name of the note list
    fk_file = None          # Foreign key of a image file
    fk_server = None        # Foreign key of server

    TABLE = "notelist"      # Name of the table

    def __init__(self, id: int, name: str, fk_server: int):
        """ # Class constructor of NoteList object 
        
        Description :
        ---
            Construct a NoteList object with parameters passed to use it more easily
        
        Access : 
        ---
            src.database.models.tables.NoteList.py\n
            NoteList.__init__()

        Parameters : 
        ---
            - id : :class:`int` => Id of the note list
            - name : :class:`str` => Name of the note list
            - fk_server : :class:`int` => Foreign key of the server id

        Returns : 
        ---
            :class:`None`
        """
        self.name = name
        self.fk_server = fk_server

        super().__init__(id)

    @staticmethod
    async def get_all_note_lists() -> dict[bool, Union[list["NoteList"], str]]:
        """ # Get all note lists function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get all the note lists stored in the database table
        
        Access : 
        ---
            src.database.models.tables.NoteList.py\n
            NoteList.get_all_note_lists()

        Returns : 
        ---
            :class:`list[NoteList]` => List of note lists
        """
        # Get the query string
        query = f"SELECT * FROM {NoteList.TABLE};"

        # Execute the query
        result = await Database.get_instance().simple_exec(query)

        # Check if the query passed
        if result.get("passed"):
            return NoteList.format_list_object(result.get("cursor"), NoteList.create_object)
        else:
            return result
        
    @staticmethod
    async def get_note_list_by_id(id_note_list: int) -> dict[bool, Union["NoteList", str]]:
        """ # Get a note list by id function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get one note list stored in the database table by its id
        
        Access : 
        ---
            src.database.models.tables.NoteList.py\n
            NoteList.get_note_list_by_id()

        Parameters : 
        ---
            - id_NoteList : :class:`int` => Searched note list id

        Returns : 
        ---
            :class:`NoteList|None` => The note list which was got in database
        """
        # Get the query string
        where = "id_noteList = %(id_noteList)s"
        query = f"SELECT * FROM {NoteList.TABLE} WHERE {where};"
        
        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"id_noteList" : id_note_list})

        # Check if the query passed
        if result.get("passed"):
            return NoteList.format_object(result.get("cursor"), NoteList.create_object)
        else:
            return result
        
    @staticmethod
    async def get_note_list_by_name(name: str) -> dict[bool, Union["NoteList", str]]:
        """ # Get a note list by name function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get one note list stored in the database table by its name
        
        Access : 
        ---
            src.database.models.tables.NoteList.py\n
            NoteList.get_note_list_by_name()

        Parameters : 
        ---
            - name : :class:`str` => Searched note list name

        Returns : 
        ---
            :class:`NoteList|None` => The note list which was got in database
        """
        # Get the query string
        where = "name = %(name)s"
        query = f"SELECT * FROM {NoteList.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"name" : name})

        # Check if the query passed
        if result.get("passed"):
            return NoteList.format_object(result.get("cursor"), NoteList.create_object)
        else:
            return result
        
    @staticmethod
    async def get_note_list_id_by_name_and_fk_server(name: str, fk_server: int) -> dict[bool, Union[int, str]]:
        """ # Get a note list id by name and fk server function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get one note list stored in the database table by its name
        
        Access : 
        ---
            src.database.models.tables.NoteList.py\n
            NoteList.get_note_list_by_name()

        Parameters : 
        ---
            - name : :class:`str` => Searched note list name

        Returns : 
        ---
            :class:`int` => the note id
        """
        # Get the query string
        where = "fk_server = %(fk_server)s AND name = %(name)s"
        query = f"SELECT id_noteList FROM {NoteList.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"name" : name, "fk_server" : fk_server})

        # Check if the query passed
        if result.get("passed"):
            return NoteList.format_object(result.get("cursor"), NoteList.create_object, True)
        else:
            return result
        
    @staticmethod
    async def get_note_list_by_name_and_fk_server(name: str, fk_server: int) -> "NoteList":
        """ # Get a note list by name and fk server function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get one note list stored in the database table by its name
        
        Access : 
        ---
            src.database.models.tables.NoteList.py\n
            NoteList.get_note_list_by_name()

        Parameters : 
        ---
            - name : :class:`str` => Searched note list name

        Returns : 
        ---
            :class:`int` => the note id
        """
        # Get the query string
        where = "fk_server = %(fk_server)s AND name = %(name)s"
        query = f"SELECT * FROM {NoteList.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"name" : name, "fk_server" : fk_server})

        # Check if the query passed
        if result.get("passed"):
            return NoteList.format_object(result.get("cursor"), NoteList.create_object)
        else:
            return result
        
    @staticmethod
    async def get_notelists_by_server_id(id_server: int) -> list["NoteList"]:
        """ # Get Notelist by server id function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get a list of Notelists using the server id
        
        Access : 
        ---
            src.database.models.tables.Notelist.py\n
            Notelist.get_Notelists_by_server_id()

        Parameters : 
        ---
            - id_server : :class:`int` => Searched server id

        Returns : 
        ---
            :class:`list[Notelist]` => A list of Notelists got
        """
        where = "fk_server = %(fk_server)s"
        query = f"SELECT * FROM {NoteList.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"fk_server" : id_server})

        # Check if the query passed
        if result.get("passed"):
            return NoteList.format_list_object(result.get("cursor"), NoteList.create_object)
        else:
            return result
        
    @staticmethod
    async def create_note_list(name: str, fk_file: int|None, fk_server: int) -> str:
        """ # Create a note list function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Create a note list in the database table
        
        Access : 
        ---
            src.database.models.tables.NoteList.py\n
            NoteList.create_note_list()

        Parameters : 
        ---
            - name : :class:`str` => Name of the note list
            - fk_server : :class:`int` => Foreign key of the server id

        Returns : 
        ---
            :class:`NoteList|None` => The note list which was created in database
        """
        # Get the query string
        fields = "(id_notelist, name, fk_file, fk_server)"
        params = "(null, %(name)s, %(fk_file)s, %(fk_server)s)"
        query = f"INSERT INTO {NoteList.TABLE} {fields} VALUES {params};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"name" : name, "fk_file" : fk_file, "fk_server" : fk_server})

        # Return the result
        return result
    
    @staticmethod
    async def delete_note_list_by_id(note_list_id: int) -> str:
        """ # Delete a note list by id function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Delete a note list in the database table by its id
        
        Access : 
        ---
            src.database.models.tables.NoteList.py\n
            NoteList.delete_note_list_by_id()

        Parameters : 
        ---
            - note_list_id : :class:`int` => Id of the note list

        Returns : 
        ---
            :class:`str` => A message which confirm the deletion
        """
        # Get the query string
        where = "id_noteList = %(id_noteList)s"
        query = f"DELETE FROM {NoteList.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"id_noteList" : note_list_id})

        # Return the result
        return result
    
    @staticmethod
    def create_object(row: list) -> "NoteList":
        """ # Create object function
        @staticmethod
        
        Description :
        ---
            Create a :class:`NoteList` object by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.NoteList.py\n
            NoteList.create_object()

        Parameters : 
        ---
            - row : :class:`list` => Row of the result

        Returns : 
        ---
            :class:`NoteList` => A NoteList object
        """
        # Create a Notelist object and return it
        id = row.get("id_note") if "id_note" in row else None
        name = row.get("name") if "name" in row else None
        fk_file = row.get("fk_file") if "fk_file" in row else None
        fk_server = row.get("fk_server") if "fk_server" in row else None

        return NoteList(id=id, name=name, fk_file=fk_file, fk_server=fk_server)