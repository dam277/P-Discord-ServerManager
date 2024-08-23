from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table
from typing import Union

class Server(Table):
    """ # Server class
        
    Description :
    ---
        Manage database Servers to use database with some specific function to retrieve some datas

    Access : 
    ---
        src.database.models.tables.Server.py\n
        Server

    inheritance : 
    ---
        - Table : :class:`Table` => Parent class of database tables
    """
    id = None               # Id of the server
    guild_id = None         # Id of the guild
    name = None             # Name of the server

    TABLE = "server"        # Name of the server table

    def __init__(self, id: int|None, guild_id: int|None, name: str|None):
        """ # Class constructor of Server object 
        
        Description :
        ---
            Construct a server object with parameters passed to use it more easily
        
        Access : 
        ---
            src.database.models.tables.Server.py\n
            Server.__init__()

        Parameters : 
        ---
            - id : :class:`int` => Id of the Server
            - guild_id : :class:`int` => Id of the guild
            - name : :class:`str` => Name of the server

        Returns : 
        ---
            :class:`None`
        """
        self.guild_id = guild_id
        self.name = name

        super().__init__(id)

    @staticmethod
    async def get_all_servers() -> dict[bool, Union[list["Server"], str]]:
        """ # Get all servers function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get all the Servers stored in the database table
        
        Access : 
        ---
            src.database.models.tables.Server.py\n
            Server.get_all_servers()

        Returns : 
        ---
            :class:`list[Server]` => List of Servers
        """
        # Get the query string
        query = f"SELECT * FROM {Server.TABLE};"
        
        # Execute the query
        result = await Database.get_instance().simple_exec(query)

        # Check if the query passed
        if result.get("passed"):
            return Server.format_list_object(result.get("cursor"), Server.create_object)
        else:
            return result
        
    @staticmethod
    async def create_server(guild_id: int, name: str) -> dict[bool, Union[MySQLCursor, str]]:
        """ # Create server function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Create a new server into the database
        
        Access : 
        ---
            src.database.models.tables.Server.py\n
            Server.create_server()

        Parameters : 
        ---
            - guild_id : :class:`int` => discord guild id
            - name : :class:`str` => Server name

        Returns : 
        ---
            :class:`str` => The message which will be sent to the user
        """
        # Get the query string
        fields = "(id_server, guildId, name)"
        params = "(null, %(guildId)s, %(name)s)"
        query = f"INSERT INTO {Server.TABLE} {fields} VALUES {params};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"guildId" : guild_id, "name" : name})
        
        # Return the result
        return result
    
    @staticmethod
    async def get_server_by_guild_id(guild_id: int) -> dict[bool, Union["Server", str]]:
        """ # Get server by guild_id id function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get a server using the guild id
        
        Access : 
        ---
            src.database.models.tables.Server.py\n
            Server.get_server_by_guild_id()

        Parameters : 
        ---
            - guild_id : :class:`int` => Searched guild id

        Returns : 
        ---
            :class:`Server` => Servers object got
        """
        # Get the query string
        where = "guildId = %(guildId)s"
        query = f"SELECT * FROM {Server.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"guildId" : guild_id})

        # Check if the query passed
        if result.get("passed"):
            return Server.format_object(result.get("cursor"), Server.create_object)
        else:
            return result
    
    @staticmethod
    async def get_server_id_by_guild_id(guild_id: int) -> dict[bool, Union[int, str]]:
        """ # Get Server id by guild id function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get a list of Server id using the guild id
        
        Access : 
        ---
            src.database.models.tables.Server\n
            Server.get_server_id_by_guild_id()

        Parameters : 
        ---
            - guild_id : :class:`int` => Searched guild id

        Returns : 
        ---
            :class:`int` => Server id
        """
        # Get the query string
        where = "guildId = %(guildId)s"
        query = f"SELECT id_server FROM {Server.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"guildId" : guild_id})

        # Check if the query passed
        if result.get("passed"):
            return Server.format_object(result.get("cursor"), Server.create_object, True)
        else:
            return result
        
    @staticmethod
    def create_object(row: dict) -> "Server":
        """ # Create object function
        @staticmethod
        
        Description :
        ---
            Create a :class:`Server` object by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.Server.py\n
            Server.create_object()

        Parameters : 
        ---
            - row : :class:`list` => Row of the result

        Returns : 
        ---
            :class:`Server` => A Server object
        """
        # Create a server object and return it
        id = row.get("id_server") if "id_server" in row else None
        guild_id = row.get("guildID") if "guildID" in row else None
        name = row.get("name") if "name" in row else None

        return Server(id=id, guild_id=guild_id, name=name)
