from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table

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
        self.id = id
        self.name = name
        self.fk_server = fk_server

    @staticmethod
    async def get_all_note_lists() -> list["NoteList"]:
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

        # Get the result by executing query into the database
        result = await Database.get_instance().simple_exec(query)
        if result[1] is True:
            return NoteList.format_list_object(result)
        else:
            return result[0]
    
    @staticmethod
    async def get_note_list_by_id(id_note_list: int) -> "NoteList":
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
        
        # Get the result by executing query into the database
        result = await Database.get_instance().bind_exec(query, {"id_noteList": id_note_list})
        if result[1] is True:
            return NoteList.format_object(result)
        else:
            return result[0]
    
    @staticmethod
    async def get_note_list_by_name(name: str) -> "NoteList":
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

        # Get the result by executing query into the database
        result = await Database.get_instance().bind_exec(query, {"name": name})
        if result[1] is True:
            return NoteList.format_object(result)
        else:
            return result[0]
    
    @staticmethod
    async def get_note_list_id_by_name_and_fk_server(name: str, fk_server: int) -> int:
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

        # Get the result by executing query into the database
        result = await Database.get_instance().bind_exec(query, {"name": name, "fk_server": fk_server})
        if result[1] is True:
            return NoteList.get_one_row(result[0])[0]
        else:
            return result[0]
        
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

        # Get the result by executing query into the database
        result = await Database.get_instance().bind_exec(query, {"name": name, "fk_server": fk_server})
        if result[1] is True:
            return NoteList.format_object(result)
        else:
            return result[0]
        
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

        # Get the result by executing query into the database
        result = await Database.get_instance().bind_exec(query, {"fk_server": id_server})
        if result[1] is True:
            return NoteList.format_list_object(result)
        else:
            return result[0]
        
    @staticmethod
    async def create_note_list(name: str, fk_server: int) -> str:
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
        fields = "(id_notelist, name, fk_server)"
        params = "(%(id_notelist)s, %(name)s, %(fk_server)s)"
        query = f"INSERT INTO {NoteList.TABLE} {fields} VALUES {params};"

        # If the server doesn't exists, insert it into the database
        result = await Database.get_instance().bind_exec(query, {"id_notelist" : None, "name": name, "fk_server": fk_server})
        if result[1] is True:
            return f"The note list **'{name}'** has been successfully created"
        else:
            return result[0]
    
    # FORMAT OBJECTS ----------------------------------------------------------------

    @staticmethod
    def format_object(cursor_result: MySQLCursor) -> "NoteList":
        """ # Format object function
        @staticmethod
        
        Description :
        ---
            Format a :class:`NoteList` object by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.NoteList.py\n
            NoteList.format_object()

        Parameters : 
        ---
            - cursor_result : :class:`MySQLCursor` => Result of the query

        Returns : 
        ---
            :class:`NoteList|None` => A NoteList object
        """
        # Getting datas from result
        row = Table.get_one_row(cursor_result[0])

        # Check if datas are filled
        if row is None or len(row) < 1:
            return None
        
        # Get the datas from the row
        note_list = NoteList.create_object(row)
        return note_list
    
    @staticmethod
    def format_list_object(cursor_result: MySQLCursor) -> list["NoteList"]:
        """ # Format list object function
        @staticmethod
        
        Description :
        ---
            Format a :class:`NoteList` object list by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.NoteList.py\n
            NoteList.format_list_object()

        Parameters : 
        ---
            - cursor_result : :class:`MySQLCursor` => Result of the query

        Returns : 
        ---
            :class:`list[NoteList]|None` => A list of NoteList object
        """
        # Getting datas from result
        rows = Table.get_all_rows(cursor_result[0])

        # Check if datas are filled
        if len(rows) < 1:
            return None
        
        # List all the servers
        note_lists = []
        for row in rows:
            # Get the datas from the row
            note_list = NoteList.create_object(row)
            note_lists.append(note_list)
        return note_lists
    
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
        # Create a server object and return it
        note_list = NoteList(id=row[0], name=row[1], fk_server=row[2])
        return note_list