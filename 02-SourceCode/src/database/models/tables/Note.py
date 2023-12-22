from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table

class Note(Table):
    id = None               # Id of the note
    title = None            # Title of the note
    text = None             # Text of the note
    fk_note_list = None     # Foreign key of notes list

    TABLE = "note"          # Name of the table

    def __init__(self, id: int|None, title: str|None, text: str|None, fk_note_list: int|None):
        """ Class constructor of a Note object 
        $param id: int => Id of the Note
        $param title: str => Title of the Note
        $param text: str => Text of the Note
        $param fk_note_list: int => Foreign key of notes list"""
        self.id = id
        self.title = title
        self.text = text
        self.fk_note_list = fk_note_list

    @staticmethod
    async def get_all_notes():
        """ Get all the notes of the database """

        # Get the query string
        query = f"SELECT * FROM {Note.TABLE};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().simple_exec(query)
        return Note.format_list_object(cursor_result)
    
    @staticmethod
    async def get_note_by_id(id_note: int):
        """ Get a note by id 
        $param id_note: int -> note id"""

        # Get the query string
        where = "id_note = %(id_note)s"
        query = f"SELECT * FROM {Note.TABLE} WHERE {where};"
        
        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"id_note": id_note})
        return Note.format_object(cursor_result)
    
    @staticmethod
    async def get_note_by_title(title: str):
        """ Get a note by title 
        $param title: str -> note title"""

        # Get the query string
        where = "title = %(title)s"
        query = f"SELECT * FROM {Note.TABLE} WHERE {where};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"title": title})
        return Note.format_object(cursor_result)
    
    # FORMAT OBJECTS ----------------------------------------------------------------

    @staticmethod
    def format_object(cursor_result: MySQLCursor):
        """ Format a database result into a object 
        $param cursor_result: MySQLCursor -> result of the query 
        Return None | Note -> None for no data, Note for successfully getting data """

        # Getting datas from result
        row = Table.get_one_row(cursor_result[0])

        # Check if datas are filled
        if row is None or len(row) < 1:
            return None
        
        # Create a note object and return it
        note = Note(id=row[0], title=row[1], description=row[2], fk_note_list=row[3])
        return note
    
    @staticmethod
    def format_list_object(cursor_result: MySQLCursor) -> list:
        """ Format a database result into a object 
        $param cursor_result: MySQLCursor -> result of the query 
        Return None | list[Note] -> None for no data, list of Notes for successfully getting datas """
        
        # Getting datas from result
        rows = Table.get_all_rows(cursor_result[0])

        # Check if datas are filled
        if len(rows) < 1:
            return None
        
        # List all the servers
        notes = list
        for row in rows:
            # Create a server object and add it to the servers list
            note = Note(id=row[0], title=row[1], description=row[2], fk_note_list=row[3])
            notes.append(note)
        return notes