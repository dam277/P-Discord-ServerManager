from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table

class Note(Table):
    """ # Note class
        
    Description :
    ---
        Manage database notes to use database with some specific function to retrieve some datas

    Access : 
    ---
        src.database.models.tables.Note.py\n
        Note

    inheritance : 
    ---
        - Table : :class:`Table` => Parent class of database tables
    """
    id = None               # Id of the note
    title = None            # Title of the note
    text = None             # Text of the note
    fk_note_list = None     # Foreign key of notes list

    TABLE = "note"          # Name of the table

    def __init__(self, id: int|None, title: str|None, text: str|None, fk_note_list: int|None):
        """ # Class constructor of Note object 
        
        Description :
        ---
            Construct a note object with parameters passed to use it more easily
        
        Access : 
        ---
            src.database.models.tables.note.py\n
            note.__init__()

        Parameters : 
        ---
            - id : :class:`int` => Id of the note
            - title : :class:`str` => Title of the note
            - text : :class:`str` => Text to the note
            - fk_note_list : :class:`int` => Foreign key of notes list

        Returns : 
        ---
            :class:`None`
        """
        self.id = id
        self.title = title
        self.text = text
        self.fk_note_list = fk_note_list

    @staticmethod
    async def get_all_notes():
        """ # Get all note function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get all the notes stored in the database table
        
        Access : 
        ---
            src.database.models.tables.Note.py\n
            Note.get_all_Notes()

        Returns : 
        ---
            :class:`list[Note]` => List of notes
        """
        # Get the query string
        query = f"SELECT * FROM {Note.TABLE};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().simple_exec(query)
        return Note.format_list_object(cursor_result)
    
    @staticmethod
    async def get_note_by_id(id_note: int):
        """ # Get a note by id function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get one note stored in the database table by its id
        
        Access : 
        ---
            src.database.models.tables.Note.py\n
            Note.get_Note_by_id()

        Parameters : 
        ---
            - id_Note : :class:`int` => Searched note id

        Returns : 
        ---
            :class:`Note|None` => The note which was got in database
        """
        # Get the query string
        where = "id_note = %(id_note)s"
        query = f"SELECT * FROM {Note.TABLE} WHERE {where};"
        
        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"id_note": id_note})
        return Note.format_object(cursor_result)
    
    @staticmethod
    async def get_note_by_title(title: str):
        """ # Get a note by title function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get one note stored in the database table by its title
        
        Access : 
        ---
            src.database.models.tables.Note.py\n
            Note.get_Note_by_title()

        Parameters : 
        ---
            - title : :class:`str` => Searched note title

        Returns : 
        ---
            :class:`Note|None` => The note which was got in database
        """
        # Get the query string
        where = "title = %(title)s"
        query = f"SELECT * FROM {Note.TABLE} WHERE {where};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"title": title})
        return Note.format_object(cursor_result)
    
    # FORMAT OBJECTS ----------------------------------------------------------------

    @staticmethod
    def format_object(cursor_result: MySQLCursor):
        """ # Format object function
        @staticmethod
        
        Description :
        ---
            Format a :class:`Note` object by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.Note.py\n
            Note.format_object()

        Parameters : 
        ---
            - cursor_result : :class:`MySQLCursor` => Result of the query

        Returns : 
        ---
            :class:`Note|None` => A note object
        """
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
        """ # Format list object function
        @staticmethod
        
        Description :
        ---
            Format a :class:`Note` object list by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.Note.py\n
            Note.format_list_object()

        Parameters : 
        ---
            - cursor_result : :class:`MySQLCursor` => Result of the query

        Returns : 
        ---
            :class:`list[Note]|None` => A list of note object
        """
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