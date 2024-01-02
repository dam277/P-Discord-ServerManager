from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table

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
        self.id = id
        self.guild_id = guild_id
        self.name = name

    @staticmethod
    async def get_all_servers():
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

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().simple_exec(query)
        return Server.format_list_object(cursor_result)

    @staticmethod
    async def create_server(guild_id: int, name: str) -> str:
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
        params = "(%(id_server)s, %(guildId)s, %(name)s)"
        query = f"INSERT INTO {Server.TABLE} {fields} VALUES {params};"

        # Get the server and define if it already exists
        obj_server = await Server.get_server_by_guild_id(guild_id)
        if obj_server is not None:
            return "The server is already created !"
        
        # If the server doesn't exists, insert it into the database
        result = await Database.get_instance().bind_exec(query, {"id_server" : None, "guildId": guild_id, "name": name})
        if result[1] is True:
            message = "Server successfully created !"
        else:
            message = result

        # Return the message to the user
        return message
    
    @staticmethod
    async def get_server_by_guild_id(guild_id: int):
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

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"guildId": guild_id})
        return Server.format_object(cursor_result)
    
    @staticmethod
    async def get_server_id_by_guild_id(guild_id: int):
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
        query = f"SELECT * FROM {Server.TABLE} WHERE {where};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"guildId": guild_id})
        return Server.format_object(cursor_result).id
    
    # FORMAT OBJECTS ----------------------------------------------------------------

    @staticmethod
    def format_object(cursor_result: MySQLCursor):
        """ # Format object function
        @staticmethod
        
        Description :
        ---
            Format a :class:`Server` object by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.Server.py\n
            Server.format_object()

        Parameters : 
        ---
            - cursor_result : :class:`MySQLCursor` => Result of the query

        Returns : 
        ---
            :class:`Server|None` => A Server object
        """
        # Getting datas from result
        row = Table.get_one_row(cursor_result[0])

        # Check if datas are filled
        if row is None or len(row) < 1:
            return None
        
        # Create a server object and return it
        server = Server(id=row[0], guild_id=row[1], name=row[2])
        return server
    
    @staticmethod
    def format_list_object(cursor_result: MySQLCursor) -> list:
        """ # Format list object function
        @staticmethod
        
        Description :
        ---
            Format a :class:`Server` object list by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.Server.py\n
            Server.format_list_object()

        Parameters : 
        ---
            - cursor_result : :class:`MySQLCursor` => Result of the query

        Returns : 
        ---
            :class:`list[Server]|None` => A list of Server object
        """
        # Getting datas from result
        rows = Table.get_all_rows(cursor_result[0])

        # Check if datas are filled
        if len(rows) < 1:
            return None
        
        # List all the servers
        servers = list
        for row in rows:
            # Create a server object and add it to the servers list
            server = Server(id=row[0], guild_id=row[1], name=row[2])
            servers.append(server)
        return servers
    
