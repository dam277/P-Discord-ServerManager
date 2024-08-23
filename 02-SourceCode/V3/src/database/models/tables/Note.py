from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table
from typing import Union

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
        self.title = title
        self.text = text
        self.fk_note_list = fk_note_list

        super().__init__(id)

    @staticmethod
    async def get_all_notes() -> dict[bool, Union[list["Note"], str]]:
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

        # Execute the query
        result = await Database.get_instance().simple_exec(query)

        # Check if the query passed
        if result.get("passed"):
            return Note.format_list_object(result.get("cursor"), Note.create_object)
        else:
            return result
        
    @staticmethod
    async def get_note_by_id(id_note: int) -> dict[bool, Union["Note", str]]:
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
        
        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"id_note" : id_note})

        # Check if the query passed
        if result.get("passed"):
            return Note.format_object(result.get("cursor"), Note.create_object)
        else:
            return result
        
    @staticmethod
    async def get_note_by_title(title: str) -> dict[bool, Union["Note", str]]:
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

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"title" : title})

        # Check if the query passed
        if result.get("passed"):
            return Note.format_object(result.get("cursor"), Note.create_object)
        else:
            return result
        
    @staticmethod
    async def add_note(title: str, text: str, fk_note_list: int) -> dict[bool, Union[MySQLCursor, str]]:
        """ # Add a note function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Add a note in the database table
        
        Access : 
        ---
            src.database.models.tables.Note.py\n
            Note.add_note()

        Parameters : 
        ---
            - title : :class:`str` => Title of the note
            - text : :class:`str` => Text of the note
            - fk_note_list : :class:`int` => Foreign key of notes list

        Returns : 
        ---
            :class:`str` => Id of the note added
        """
        # Get the query string
        fields = "(id_note, title, text, fk_noteList)"
        params = "(null, %(title)s, %(text)s, %(fk_noteList)s)"
        query = f"INSERT INTO {Note.TABLE} {fields} VALUES {params};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"title" : title, "text" : text, "fk_noteList" : fk_note_list})

        # Return the result
        return result
    
    @staticmethod
    async def get_notes_by_note_list_id(note_list_id: int) -> dict[bool, Union[list["Note"], str]]:
        """ # Get notes by note list id function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get all notes stored in the database table by the note list id
        
        Access : 
        ---
            src.database.models.tables.Note.py\n
            Note.get_notes_by_note_list_id()

        Parameters : 
        ---
            - note_list_id : :class:`int` => Note list id

        Returns : 
        ---
            :class:`list[Note]|None` => List of notes
        """
        # Get the query string
        where = "fk_noteList = %(fk_noteList)s"
        query = f"SELECT * FROM {Note.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"fk_noteList" : note_list_id})
        
        # Check if the query passed
        if result.get("passed"):
            return Note.format_list_object(result.get("cursor"), Note.create_object)
        else:
            return result
        
    @staticmethod
    async def get_notes_in_notelists_by_server_id(server_id: int) -> dict[bool, Union[list["Note"], str]]:
        """ # Get notes in notelists by server id function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Get all notes stored in the database table by the server id
        
        Access : 
        ---
            src.database.models.tables.Note.py\n
            Note.get_notes_in_notelists_by_server_id()

        Parameters : 
        ---
            - server_id : :class:`int` => Server id

        Returns : 
        ---
            :class:`list[Note]|None` => List of notes
        """
        # Get the query string
        inner_select_server_id = "SELECT id_noteList FROM noteList WHERE fk_server = %(fk_server)s"
        where = f"fk_noteList IN ({inner_select_server_id})"
        query = f"SELECT * FROM {Note.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"fk_server" : server_id})

        # Check if the query passed
        if result.get("passed"):
            return Note.format_list_object(result.get("cursor"), Note.create_object)
        else:
            return result
        
    @staticmethod
    async def get_note_in_notelists_by_server_id_and_note_title(server_id: int, note_title: str) -> dict[bool, Union["Note", str]]:
        """ # Get a note in notelists by server id and note title function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Get all notes stored in the database table by the server id and note title
        
        Access : 
        ---
            src.database.models.tables.Note.py\n
            Note.get_notes_in_notelists_by_server_id_and_note_title()

        Parameters : 
        ---
            - server_id : :class:`int` => Server id
            - note_title : :class:`str` => Note title

        Returns : 
        ---
            :class:`list[Note]|None` => List of notes
        """
        # Get the query string
        inner_select_server_id = "SELECT id_noteList FROM noteList WHERE fk_server = %(fk_server)s"
        where = f"fk_noteList IN ({inner_select_server_id}) AND title = %(title)s"
        query = f"SELECT * FROM {Note.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"fk_server" : server_id, "title" : note_title})

        # Check if the query passed
        if result.get("passed"):
            return Note.format_object(result.get("cursor"), Note.create_object)
        else:
            return result
        
    @staticmethod
    async def update_note(note_id: int, new_title: str, new_text: str) -> dict[bool, Union[MySQLCursor, str]]:
        """ # Update note function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Update a note stored in the database table
        
        Access : 
        ---
            src.database.models.tables.Note.py\n
            Note.update_note()

        Parameters : 
        ---
            - note_id : :class:`int` => Note id
            - new_title : :class:`str` => New title of the note
            - new_text : :class:`str` => New text of the note

        Returns : 
        ---
            :class:`str` => Message of the result
        """
        # Get the query string
        where = "id_note = %(id_note)s"
        set = "title = %(title)s, text = %(text)s"
        query = f"UPDATE {Note.TABLE} SET {set} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"id_note" : note_id, "title" : new_title, "text" : new_text})

        # Return the result
        return result
    
    @staticmethod
    async def delete_note_by_id(id_note: int) -> dict[bool, Union[MySQLCursor, str]]:
        """ # Delete note by id function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Delete a note stored in the database table by its id
        
        Access : 
        ---
            src.database.models.tables.Note.py\n
            Note.delete_note_by_id()

        Parameters : 
        ---
            - id_note : :class:`int` => Note id

        Returns : 
        ---
            :class:`str` => Message of the result
        """
        # Get the query string
        where = "id_note = %(id_note)s"
        query = f"DELETE FROM {Note.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"id_note" : id_note})

        # Return the result
        return result
    
    @staticmethod
    async def delete_notes_by_id_notelist(note_list_id: int) -> dict[bool, Union[MySQLCursor, str]]:
        """ # Delete notes by id notelist function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Delete all notes stored in the database table by the note list id
        
        Access : 
        ---
            src.database.models.tables.Note.py\n
            Note.delete_notes_by_id_notelist()

        Parameters : 
        ---
            - note_list_id : :class:`int` => Note list id

        Returns : 
        ---
            :class:`str` => Message of the result
        """
        # Get the query string
        where = "fk_noteList = %(fk_noteList)s"
        query = f"DELETE FROM {Note.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"fk_noteList" : note_list_id})

        # Return the result
        return result

    @staticmethod
    def create_object(row: list) -> "Note":
        """ # Create object function
        @staticmethod
        
        Description :
        ---
            Create a :class:`Note` object by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.Note.py\n
            Note.create_object()

        Parameters : 
        ---
            - row : :class:`list` => Row of the result

        Returns : 
        ---
            :class:`Note` => A Note object
        """
        # Create a note object and return it
        id = row.get("id_note") if "id_note" in row else None
        title = row.get("title") if "title" in row else None
        text = row.get("text") if "text" in row else None
        fk_note_list = row.get("fk_noteList") if "fk_noteList" in row else None

        return Note(id=id, title=title, text=text, fk_note_list=fk_note_list)