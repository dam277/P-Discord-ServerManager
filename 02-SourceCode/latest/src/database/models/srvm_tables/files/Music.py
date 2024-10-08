from mysql.connector.cursor import MySQLCursor
from ....Database import Database
from ..File import File

from typing import Union

class Music(File):
    """ # Music class
        
    Description :
    ---
        Manage database musics to use database with some specific function to retrieve some datas

    Access : 
    ---
        src.database.models.tables.files.Music.py\n
        Music

    inheritance : 
    ---
        - File : :class:`File` => Parent class of database Files
    """
    TABLE = "music"          # Database table name

    def __init__(self, id: int, name: str, path: str, fk_server: int):
        """ # Class constructor of Music object 
        
        Description :
        ---
            Construct a Music object with parameters passed to use it more easily
        
        Access : 
        ---
            src.database.models.tables.files.Music.py\n
            Music.__init__()

        Parameters : 
        ---
            - id : :class:`int` => Id of the Music
            - name : :class:`str` => Name of the Music
            - path : :class:`str` => Path to the Music
            - fk_server : :class:`int` => Foreign key of the server id

        Returns : 
        ---
            :class:`None`
        """
        super().__init__(id, name, path, fk_server)

    @staticmethod
    async def get_all_files() -> dict[bool, Union[list["Music"], str]]:
        """ # Get all Music function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get all the musics stored in the database table
        
        Access : 
        ---
            src.database.models.tables.Music.py\n
            Music.get_all_files()

        Returns : 
        ---
            :class:`list[File]` => List of musics
        """
        # Get the query string
        # Get the query string
        inner_join_file = f"INNER JOIN file ON {Music.TABLE}.id_file = {File.TABLE}.id_file"
        query = f"SELECT * FROM {Music.TABLE} {inner_join_file};"

        # Execute the query
        result = await Database.get_instance(Music.DATABASE).simple_exec(query)

        # Check if the query passed
        if result.get("passed"):
            return Music.format_list_object(result.get("cursor"), Music.create_object)
        else:
            return result

    @staticmethod
    async def get_musics_by_server_id(id_server) -> dict[bool, Union[list["Music"], str]]:
        """ # Get all Music function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get all the musics stored in the database table

        Parameters :
        ---
            - id_server : :class:`int` => Id of the server
        
        Access : 
        ---
            src.database.models.tables.Music.py\n
            Music.get_all_musics()
        
        Returns : 
        ---
            :class:`list[File]` => List of musics
        """
        # Get the query string
        # Get the query string
        inner_join_file = f"INNER JOIN file ON {Music.TABLE}.id_file = {File.TABLE}.id_file"
        where = f"fk_server = %(id_server)s"
        query = f"SELECT * FROM {Music.TABLE} {inner_join_file} where {where};"

        # Execute the query
        result = await Database.get_instance(Music.DATABASE).bind_exec(query, {"id_server" : id_server})

        # Check if the query passed
        if result.get("passed"):
            return Music.format_list_object(result.get("cursor"), Music.create_object)
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
            query = f"INSERT INTO {Music.TABLE} {fields} VALUES {params};"

            # Get the last file id
            file_id_result = await File.get_last_file_id()

            # Execute the query
            result = await Database.get_instance(Music.DATABASE).bind_exec(query, {"id_file" : file_id_result.get("value")})

        # Return the result
        return result
    
    @staticmethod
    async def get_musics_by_playlist_id(id_playlist: int) -> dict[bool, Union[list["Music"], str]]:
        """ # Get musics by playlist id method

        Description :
        ---
            This method is used to get the musics from a playlist id

        Access :
        ---
            src.database.models.srvm_tables.Music
            Music.get_musics_from_playlist_id()

        Parameters :
        ---
            - id_playlist : :class:`int` => The id of the playlist

        Returns :
        ---
            :class:`list` => A list of musics from the playlist id
        """
        # Get the query
        where = "id_playlist = %(id_playlist)s"
        inner_join = "music_playlist ON music_playlist.id_file = file.id_file"
        query = f"SELECT file.id_file, name, path, fk_server FROM {File.TABLE} INNER JOIN {inner_join} WHERE {where}"

        # Get the result
        result = await Database.get_instance(Music.DATABASE).bind_exec(query, {"id_playlist": id_playlist})
        
        # Check if the query passed
        if result.get("passed"):
            return Music.format_list_object(result.get("cursor"), Music.create_object)
        else:
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
        query = f"DELETE FROM {Music.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance(Music.DATABASE).bind_exec(query, {"id_file" : id_file})

        # Check if the query passed
        if result.get("passed"):
            return await File.delete_file_by_id(id_file)
        else:
            return result
        