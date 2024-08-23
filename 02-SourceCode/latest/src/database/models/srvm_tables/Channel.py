from mysql.connector.cursor import MySQLCursor

from ....utils.enums.Databases import Databases
from ...Database import Database
from ..Table import Table

from typing import Union

class Channel(Table):
    """ # channel class
    
    Description :
    ---
        This class is used to represent a  channel in the database
    
    Access : 
    ---
        src.database.models.tables.Channel 
        Channel
    
    Inheritance :
    ---
        - Table : :class:`Table` => Parent class of database tables
    """
    id = None
    channelID = None
    fk_server = None
    fk_channelType = None

    TABLE = "channel"
    DATABASE = Databases.server_manager # Database of the server table

    def __init__(self, id: int, channelID: int, fk_server: int, fk_channelType: int):
        """ # Constructor method
        
        Description :
        ---
            Initializes the attributes of the class

        Access :
        ---
            src.database.models.tables.Channel
            Channel.__init__()

        Parameters :
        ---
            - id : :class:`int` => The id of the  channel
            - channelID : :class:`int` => The id of the channel
            - fk_server : :class:`int` => The id of the server

        Returns :
        ---
            :class:`None`
        """
        self.channelID = channelID
        self.fk_server = fk_server
        self.fk_channelType = fk_channelType

        super().__init__(id)

    @staticmethod
    async def get_channels_by_guild_id(guild_id: int) -> dict[bool, Union[list["Channel"], str]]:
        """ # Get channels by server id
        
        Description :
        ---
            Get all  channel of a server

        Access :
        ---
            src.database.models.tables.Channel
            Channel.get_channel_by_server_id()

        Parameters :
        ---
            - server_id : :class:`int` => The id of the server

        Returns :
        ---
            :class:`list` => List of  channel
        """
        # Get the query string
        inner_join_server = "INNER JOIN server ON channel.fk_server = server.id_server"
        where = "server.guildID = %(guildID)s"
        query = f"SELECT id_channel, channelID, fk_channelType, fk_server FROM {Channel.TABLE} {inner_join_server} WHERE {where};"

        # Execute the query
        result = await Database.get_instance(Channel.DATABASE).bind_exec(query, {"guildID" : guild_id})
        
        # Check if the query passed
        if result.get("passed"):
            return Channel.format_list_object(result.get("cursor"), Channel.create_object)
        else:
            return result
        
    @staticmethod
    async def get_channel_by_guild_id_and_type_id(guild_id: int, channelType_id: int) -> dict[bool, Union["Channel", str]]:
        """ # Get channel by server id
        
        Description :
        ---
            Get all  channel of a server

        Access :
        ---
            src.database.models.tables.Channel
            Channel.get_channel_by_server_id()

        Parameters :
        ---
            - server_id : :class:`int` => The id of the server

        Returns :
        ---
            :class:`list` => List of  channel
        """
        # Get the query string
        inner_join_server = "INNER JOIN server ON channel.fk_server = server.id_server"
        where = "server.guildID = %(guildID)s and fk_channelType = %(fk_channelType)s"
        query = f"SELECT * FROM {Channel.TABLE} {inner_join_server} WHERE {where};"

        # Execute the query
        result = await Database.get_instance(Channel.DATABASE).bind_exec(query, {"guildID" : guild_id, "fk_channelType" : channelType_id})

        # Check if the query passed
        if result.get("passed"):
            return Channel.format_object(result.get("cursor"), Channel.create_object)
        else:
            return result
        
    @staticmethod
    async def get_channel_by_id(channel_id: int) -> dict[bool, Union["Channel", str]]:
        """ # Get channel by channel id
        
        Description :
        ---
            Get all  channel of a server

        Access :
        ---
            src.database.models.tables.Channel
            Channel.get_channel_by_server_id()

        Parameters :
        ---
            - server_id : :class:`int` => The id of the server

        Returns :
        ---
            :class:`list` => List of  channel
        """
        # Get the query string
        where = "channelID = %(channelID)s"
        query = f"SELECT * FROM {Channel.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance(Channel.DATABASE).bind_exec(query, {"channelID" : channel_id})

        # Check if the query passed
        if result.get("passed"):
            return Channel.format_object(result.get("cursor"), Channel.create_object)
        else:
            return result
        
    @staticmethod
    async def create_channel(channel_id: int, server_id: int, channel_type_id: int) -> dict[bool, Union[MySQLCursor, str]]:
        """ # Create channel
        
        Description :
        ---
            Create a  channel

        Access :
        ---
            src.database.models.tables.Channel
            Channel.create_channel()

        Parameters :
        ---
            - channel_id : :class:`int` => The id of the channel
            - server_id : :class:`int` => The id of the server

        Returns :
        ---
            :class:`Channel` => The  channel
        """
        # Get the query string
        fields = "(id_channel, channelID, fk_channelType, fk_server)"
        params = "(null, %(channelID)s, %(fk_channelType)s, %(fk_server)s)"
        query = f"INSERT INTO {Channel.TABLE} {fields} VALUES {params};"

        # Execute the query
        result = await Database.get_instance(Channel.DATABASE).bind_exec(query, {"channelID" : channel_id, "fk_channelType" : channel_type_id, "fk_server" : server_id})

        # Return the result
        return result
        
    @staticmethod 
    async def delete_channel_by_id(id__channel: int) -> dict[bool, Union[MySQLCursor, str]]:
        """ # Delete channel
        
        Description :
        ---
            Delete a  channel

        Access :
        ---
            src.database.models.tables.Channel
            Channel.delete_channel()

        Parameters :
        ---
            - id__channel : :class:`int` => The id of the channel

        Returns :
        ---
            :class:`Channel` => The  channel
        """
        # Get the query string
        where = "id_channel = %(id_channel)s"
        query = f"DELETE FROM {Channel.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance(Channel.DATABASE).bind_exec(query, {"id_channel" : id__channel})

        # Return the result
        return result
    
    @staticmethod
    def create_object(row: list) -> "Channel":
        """ # Create object function
        @staticmethod
        
        Description :
        ---
            Create a :class:`Channel` object by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.Channel.py\n
            Channel.create_object()

        Parameters : 
        ---
            - row : :class:`list` => Row of the result

        Returns : 
        ---
            :class:`Channel` => A Channel object
        """
        # Create a Channel object and return it
        id = row.get("id_channel") if "id_channel" in row else None
        channelID = row.get("channelID") if "channelID" in row else None
        fk_server = row.get("fk_server") if "fk_server" in row else None
        fk_channelType = row.get("fk_channelType") if "fk_channelType" in row else None

        return Channel(id=id, channelID=channelID, fk_server=fk_server, fk_channelType=fk_channelType)