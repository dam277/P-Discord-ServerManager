from mysql.connector.cursor import MySQLCursor

from ....utils.enums.Databases import Databases

from ...Database import Database

from ..Table import Table
from typing import Union

class DistantServer(Table):
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
    adress = None           # Adress of the server
    port = None             # Port of the server
    fk_server = None        # Foreign key of the server

    TABLE = "distantServer"        # Name of the server table
    DATABASE = Databases.server_manager # Database of the server table

    def __init__(self, id: int, adress: str, port: int, fk_server: int):
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
            - id_server : :class:`int` => Id of the guild
            - name : :class:`str` => Name of the server

        Returns : 
        ---
            :class:`None`
        """
        self.adress = adress
        self.port = port
        self.fk_server = fk_server

        super().__init__(id)

    @staticmethod
    async def get_all_distant_servers() -> dict[bool, Union[list["DistantServer"], str]]:
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
        query = f"SELECT * FROM {DistantServer.TABLE};"
        
        # Execute the query
        result = await Database.get_instance(DistantServer.DATABASE).simple_exec(query)

        # Check if the query passed
        if result.get("passed"):
            return DistantServer.format_list_object(result.get("cursor"), DistantServer.create_object)
        else:
            return result
        
    @staticmethod
    async def add_distant_server(adress: str, port: int, id_server) -> dict[bool, Union[MySQLCursor, str]]:
        """ # add server function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            add a new server into the database
        
        Access : 
        ---
            src.database.models.tables.Server.py\n
            Server.add_server()

        Parameters : 
        ---
            - id_server : :class:`int` => discord id
            - name : :class:`str` => Server name

        Returns : 
        ---
            :class:`str` => The message which will be sent to the user
        """
        # Get the query string
        fields = "(id_distantServer, adress, port, fk_server)"
        params = "(null, %(adress)s, %(port)s, %(fk_server)s)"
        query = f"INSERT INTO {DistantServer.TABLE} {fields} VALUES {params};"

        # Execute the query
        result = await Database.get_instance(DistantServer.DATABASE).bind_exec(query, {"adress" : adress, "port" : port, "fk_server" : id_server})
        
        # Return the result
        return result
    
    @staticmethod
    async def get_distant_servers_by_server_id(id_server: int) -> dict[bool, Union[list["DistantServer"], str]]:
        """ # Get DistantServer by id_server id function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get a DistantServer using the guild id
        
        Access : 
        ---
            src.database.models.tables.DistantServer.py\n
            DistantServer.get_DistantServer_by_id_server()

        Parameters : 
        ---
            - id_server : :class:`int` => Searched guild id

        Returns : 
        ---
            :class:`DistantServer` => DistantServers object got
        """
        # Get the query string
        where = "fk_server = %(fk_server)s"
        query = f"SELECT * FROM {DistantServer.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance(DistantServer.DATABASE).bind_exec(query, {"fk_server" : id_server})

        # Check if the query passed
        if result.get("passed"):
            return DistantServer.format_list_object(result.get("cursor"), DistantServer.create_object)
        else:
            return result
        
    @staticmethod
    async def get_distant_servers_by_guild_id(guild_id: int) -> dict[bool, Union[list["DistantServer"], str]]:
        """ # Get DistantServer by guild_id id function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            Get a DistantServer using the guild id
        
        Access : 
        ---
            src.database.models.tables.DistantServer.py\n
            DistantServer.get_DistantServer_by_id_server()

        Parameters : 
        ---
            - id_server : :class:`int` => Searched guild id

        Returns : 
        ---
            :class:`DistantServer` => DistantServers object got
        """
        # Get the query string
        inner_select_guild_id = "SELECT id_server FROM server WHERE guildID = %(guild_id)s"
        where = f"fk_server = ({inner_select_guild_id})"
        query = f"SELECT * FROM {DistantServer.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance(DistantServer.DATABASE).bind_exec(query, {"guild_id" : guild_id})

        # Check if the query passed
        if result.get("passed"):
            return DistantServer.format_list_object(result.get("cursor"), DistantServer.create_object)
        else:
            return result
        
    @staticmethod
    async def delete_distant_server_by_server_id_and_distant_server(id_server: int, adress: str, port: int):
        """ # delete distant server server function
        /!\\ This is a coroutine, it needs to be awaited
        @staticmethod
        
        Description :
        ---
            delete a distant server from the database
        
        Access : 
        ---
            src.database.models.tables.Server.py\n
            Server.delete_distant_server()

        Parameters : 
        ---
            - id_server : :class:`int` => discord server id
            - adress : :class:`str` => distant server adress
            - port : :class:`int` => distant server port

        Returns : 
        ---
            :class:`str` => The message which will be sent to the user
        """
        # Get the query string
        where = "fk_server = %(fk_server)s AND adress = %(adress)s AND port = %(port)s"
        query = f"DELETE FROM {DistantServer.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance(DistantServer.DATABASE).bind_exec(query, {"adress" : adress, "port" : port, "fk_server" : id_server})
        
        # Return the result
        return result
        
    @staticmethod
    def create_object(row: dict) -> "DistantServer":
        """ # Create object function
        @staticmethod
        
        Description :
        ---
            Create a :class:`DistantServer` object by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.DistantServer.py\n
            DistantServer.create_object()

        Parameters : 
        ---
            - row : :class:`list` => Row of the result

        Returns : 
        ---
            :class:`DistantServer` => A DistantServer object
        """
        # Create a DistantServer object and return it
        id = row.get("id_distantServer") if "id_distantServer" in row else None
        adress = row.get("adress") if "adress" in row else None
        port = row.get("port") if "port" in row else None
        fk_server = row.get("fk_server") if "fk_server" in row else None        

        return DistantServer(id=id, adress=adress, port=port, fk_server=fk_server)
