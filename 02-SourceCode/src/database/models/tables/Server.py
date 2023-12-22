from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table

class Server(Table):
    id = None               # Id of the server
    guild_id = None         # Id of the guild
    name = None             # Name of the server

    TABLE = "server"        # Name of the server table

    def __init__(self, id: int|None, guild_id: int|None, name: str|None):
        """ Class constructor of a Server object 
        $param id: int => Id of the Server
        $param guild_id: int => guild_id of the Server
        $param name: str => name to the Server """
        self.id = id
        self.guild_id = guild_id
        self.name = name

    @staticmethod
    async def get_all_servers():
        """ Get all the servers of the database """

        # Get the query string
        query = f"SELECT * FROM {Server.TABLE};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().simple_exec(query)
        return Server.format_list_object(cursor_result)

    @staticmethod
    async def create_server(guild_id: int, name: str) -> str:
        """ Create a server into the database 
        $param guild_id: Guild -> Discord server id
        $param name: string -> Discord server name
        Return message: str -> Message to send to the server"""

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
        """ Get a server by guild id
        $param guild_id: int -> Discord server id
        Return format_object()"""

        # Get the query string
        where = "guildId = %(guildId)s"
        query = f"SELECT * FROM {Server.TABLE} WHERE {where};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"guildId": guild_id})
        return Server.format_object(cursor_result)
    
    @staticmethod
    async def get_server_id_by_guild_id(guild_id: int):
        """ Get a server id by guild id
        $param guild_id: int -> Discord server id
        Return format_object()"""

        # Get the query string
        where = "guildId = %(guildId)s"
        query = f"SELECT id_server FROM {Server.TABLE} WHERE {where};"

        # Get the result by executing query into the database
        cursor_result = await Database.get_instance().bind_exec(query, {"guildId": guild_id})
        return Server.format_object(cursor_result).id
    
    # FORMAT OBJECTS ----------------------------------------------------------------

    @staticmethod
    def format_object(cursor_result: MySQLCursor):
        """ Format a database result into a object 
        $param cursor_result: MySQLCursor -> result of the query 
        Return None | Server -> None for no data, Server for successfully getting data """

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
        """ Format a database result into a object 
        $param cursor_result: MySQLCursor -> result of the query 
        Return None | list[Server] -> None for no data, list of servers for successfully getting datas """
        
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
    
