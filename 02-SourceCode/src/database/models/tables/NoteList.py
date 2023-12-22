from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table

class NoteList(Table):
    id = None               # Id of the note list
    name = None             # Name of the note list
    fk_server = None        # Foreign key of server

    TABLE = "notelist"      # Name of the table

    def __init__(self, id: int|None, name: str|None, fk_server: int|None):
        """ Class constructor of a Note object 
        $param id: int => Id of the Note
        $param name: str => Name of the Note
        $param fk_server: int => Foreign key of server"""
        self.id = id
        self.name = name
        self.fk_server = fk_server

    @staticmethod
    async def get_all_note_lists():
        """ Get all the note lists of the database """

        # Get the query string
        query = f"SELECT * FROM {NoteList.TABLE};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().simple_exec(query)
        return NoteList.format_list_object(cursor_result)
    
    @staticmethod
    async def get_note_list_by_id(id_note_list: int):
        """ Get a note list by id 
        $param id_note_list: int -> note id"""

        # Get the query string
        where = "id_noteList = %(id_noteList)s"
        query = f"SELECT * FROM {NoteList.TABLE} WHERE {where};"
        
        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"id_noteList": id_note_list})
        return NoteList.format_object(cursor_result)
    
    @staticmethod
    async def get_note_list_by_name(name: str):
        """ Get a note list by name 
        $param name: str -> note list name"""

        # Get the query string
        where = "name = %(name)s"
        query = f"SELECT * FROM {NoteList.TABLE} WHERE {where};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"name": name})
        return NoteList.format_object(cursor_result)
    
    # FORMAT OBJECTS ----------------------------------------------------------------

    @staticmethod
    def format_object(cursor_result: MySQLCursor):
        """ Format a database result into a object 
        $param cursor_result: MySQLCursor -> result of the query 
        Return None | Note list -> None for no data, Note list for successfully getting data """

        # Getting datas from result
        row = Table.get_one_row(cursor_result[0])

        # Check if datas are filled
        if row is None or len(row) < 1:
            return None
        
        # Create a note object and return it
        note_list = NoteList(id=row[0], name=row[1], fk_server=row[2])
        return note_list
    
    @staticmethod
    def format_list_object(cursor_result: MySQLCursor) -> list:
        """ Format a database result into a object 
        $param cursor_result: MySQLCursor -> result of the query 
        Return None | list[NoteList] -> None for no data, list of Note lists for successfully getting datas """
        
        # Getting datas from result
        rows = Table.get_all_rows(cursor_result[0])

        # Check if datas are filled
        if len(rows) < 1:
            return None
        
        # List all the servers
        note_lists = list
        for row in rows:
            # Create a server object and add it to the servers list
            note_list = NoteList(id=row[0], name=row[1], fk_server=row[2])
            note_lists.append(note_list)
        return note_lists