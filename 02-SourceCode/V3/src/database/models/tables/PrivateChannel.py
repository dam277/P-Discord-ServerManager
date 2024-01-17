from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table

from typing import Union

class PrivateChannel(Table):
    """ # Private channel class
    
    Description :
    ---
        This class is used to represent a private channel in the database
    
    Access : 
    ---
        src.database.models.tables.PrivateChannel 
        PrivateChannel
    
    Inheritance :
    ---
        - Table : :class:`Table` => Parent class of database tables
    """
    id = None
    channelID = None
    fk_server = None

    TABLE = "privatechannel"

    def __init__(self, id: int, channelID: int, fk_server: int):
        """ # Constructor method
        
        Description :
        ---
            Initializes the attributes of the class

        Access :
        ---
            src.database.models.tables.PrivateChannel
            PrivateChannel.__init__()

        Parameters :
        ---
            - id : :class:`int` => The id of the private channel
            - channelID : :class:`int` => The id of the channel
            - fk_server : :class:`int` => The id of the server

        Returns :
        ---
            :class:`None`
        """
        self.channelID = channelID
        self.fk_server = fk_server

        super().__init__(id)

    @staticmethod
    async def get_channel_by_guild_id(guild_id: int) -> dict[bool, Union["PrivateChannel", str]]:
        """ # Get channel by server id
        
        Description :
        ---
            Get all private channel of a server

        Access :
        ---
            src.database.models.tables.PrivateChannel
            PrivateChannel.get_channel_by_server_id()

        Parameters :
        ---
            - server_id : :class:`int` => The id of the server

        Returns :
        ---
            :class:`list` => List of private channel
        """
        # Get the query string
        inner_join_server = "INNER JOIN server ON privatechannel.fk_server = server.id_server"
        where = "server.guildID = %(guildID)s"
        query = f"SELECT id_privateChannel, fk_server, channelID FROM {PrivateChannel.TABLE} {inner_join_server} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"guildID" : guild_id})

        # Check if the query passed
        if result.get("passed"):
            return PrivateChannel.format_object(result.get("cursor"), PrivateChannel.create_object)
        else:
            return result
        
    @staticmethod
    async def get_channel_by_channel_id(channel_id: int) -> dict[bool, Union["PrivateChannel", str]]:
        """ # Get channel by channel id
        
        Description :
        ---
            Get all private channel of a server

        Access :
        ---
            src.database.models.tables.PrivateChannel
            PrivateChannel.get_channel_by_server_id()

        Parameters :
        ---
            - server_id : :class:`int` => The id of the server

        Returns :
        ---
            :class:`list` => List of private channel
        """
        # Get the query string
        where = "id_channel = %(id_channel)s"
        query = f"SELECT * FROM {PrivateChannel.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"id_channel" : channel_id})

        # Check if the query passed
        if result.get("passed"):
            return PrivateChannel.format_object(result.get("cursor"), PrivateChannel.create_object)
        else:
            return result
        
    @staticmethod
    async def create_channel(channel_id: int, server_id: int) -> dict[bool, Union[MySQLCursor, str]]:
        """ # Create channel
        
        Description :
        ---
            Create a private channel

        Access :
        ---
            src.database.models.tables.PrivateChannel
            PrivateChannel.create_channel()

        Parameters :
        ---
            - channel_id : :class:`int` => The id of the channel
            - server_id : :class:`int` => The id of the server

        Returns :
        ---
            :class:`PrivateChannel` => The private channel
        """
        # Get the query string
        fields = "(id_privateChannel, fk_server, channelID)"
        params = "(null, %(fk_server)s, %(channelID)s)"
        query = f"INSERT INTO {PrivateChannel.TABLE} {fields} VALUES {params};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"id_privateChannel" : None, "fk_server" : server_id, "channelID" : channel_id})

        # Return the result
        return result
        
    @staticmethod 
    async def delete_channel_by_id(channel_id: int) -> dict[bool, Union[MySQLCursor, str]]:
        """ # Delete channel
        
        Description :
        ---
            Delete a private channel

        Access :
        ---
            src.database.models.tables.PrivateChannel
            PrivateChannel.delete_channel()

        Parameters :
        ---
            - channel_id : :class:`int` => The id of the channel

        Returns :
        ---
            :class:`PrivateChannel` => The private channel
        """
        # Get the query string
        where = "channelID = %(channelID)s"
        query = f"DELETE FROM {PrivateChannel.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance().bind_exec(query, {"channelID" : channel_id})

        # Return the result
        return result
    
    @staticmethod
    def create_object(row: list) -> "PrivateChannel":
        """ # Create object function
        @staticmethod
        
        Description :
        ---
            Create a :class:`PrivateChannel` object by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.PrivateChannel.py\n
            PrivateChannel.create_object()

        Parameters : 
        ---
            - row : :class:`list` => Row of the result

        Returns : 
        ---
            :class:`PrivateChannel` => A PrivateChannel object
        """
        # Create a PrivateChannel object and return it
        id = row.get("id_privateChannel") if "id_privateChannel" in row else None
        channelID = row.get("channelID") if "channelID" in row else None
        fk_server = row.get("fk_server") if "fk_server" in row else None

        return PrivateChannel(id=id, channelID=channelID, fk_server=fk_server)
