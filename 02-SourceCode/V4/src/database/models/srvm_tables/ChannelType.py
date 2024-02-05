from os import name
from mysql.connector.cursor import MySQLCursor

from ....utils.enums.Databases import Databases
from ...Database import Database
from ..Table import Table

from typing import Union

class ChannelType(Table):
    """ # channelType class
    
    Description :
    ---
        This class is used to represent a  channelType in the database
    
    Access : 
    ---
        src.database.models.tables.channelType 
        channelType
    
    Inheritance :
    ---
        - Table : :class:`Table` => Parent class of database tables
    """
    id = None
    name = None

    TABLE = "channelType"
    DATABASE = Databases.server_manager # Database of the server table

    def __init__(self, id: int, name: str):
        """ # Constructor method
        
        Description :
        ---
            Initializes the attributes of the class

        Access :
        ---
            src.database.models.tables.Channel
            ChannelType.__init__()

        Parameters :
        ---
            - id : :class:`int` => The id of the  channel
            - name : :class:`str` => The name of the channel

        Returns :
        ---
            :class:`None`
        """
        self.name = name

        super().__init__(id)

    @staticmethod
    async def get_all_channel_types() -> dict[bool, Union[list["ChannelType"], str]]:
        """ # Get channels by server id
        
        Description :
        ---
            Get all  channel of a server

        Access :
        ---
            src.database.models.tables.Channel
            ChannelType.get_channel_by_server_id()

        Parameters :
        ---
            - server_id : :class:`int` => The id of the server

        Returns :
        ---
            :class:`list` => List of  channel
        """
        # Get the query string
        query = f"SELECT * FROM {ChannelType.TABLE};"

        # Execute the query
        result = await Database.get_instance(ChannelType.DATABASE).simple_exec(query)

        # Check if the query passed
        if result.get("passed"):
            return ChannelType.format_list_object(result.get("cursor"), ChannelType.create_object)
        else:
            return result
    
    @staticmethod
    async def get_channel_type_id_by_name(name: str) -> dict[bool, Union[int, str]]:
        """ # Get channel type id by name
        
        Description :
        ---
            Get a channel type id by its name

        Access :
        ---
            src.database.models.tables.Channel
            ChannelType.get_channel_id_by_name()

        Parameters :
        ---
            - name : :class:`str` => The name of the channel

        Returns :
        ---
            :class:`Channel` => A Channel object
        """
        # Get the query string
        where = "name = %(name)s"
        query = f"SELECT id_channelType FROM {ChannelType.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance(ChannelType.DATABASE).bind_exec(query, {"name" : name})

        # Check if the query passed
        if result.get("passed"):
            return ChannelType.format_object(result.get("cursor"), ChannelType.create_object, True)
        else:
            return result

    @staticmethod
    async def get_channel_type_by_name(name: str) -> dict[bool, Union["ChannelType", str]]:
        """ # Get channel type by name
        
        Description :
        ---
            Get a channel by its name

        Access :
        ---
            src.database.models.tables.Channel
            ChannelType.get_channel_by_name()

        Parameters :
        ---
            - name : :class:`str` => The name of the channel

        Returns :
        ---
            :class:`Channel` => A Channel object
        """
        # Get the query string
        where = "name = %(name)s"
        query = f"SELECT * FROM {ChannelType.TABLE} WHERE {where};"

        # Execute the query
        result = await Database.get_instance(ChannelType.DATABASE).bind_exec(query, {"name" : name})

        # Check if the query passed
        if result.get("passed"):
            return ChannelType.format_object(result.get("cursor"), ChannelType.create_object)
        else:
            return result

    @staticmethod
    def create_object(row: list) -> "ChannelType":
        """ # Create object function
        @staticmethod
        
        Description :
        ---
            Create a :class:`Channel` object by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.ChannelType.py\n
            ChannelType.create_object()

        Parameters : 
        ---
            - row : :class:`list` => Row of the result

        Returns : 
        ---
            :class:`Channel` => A Channel object
        """
        # Create a Channel object and return it
        id = row.get("id_Channel") if "id_Channel" in row else None
        name = row.get("name") if "name" in row else None

        return ChannelType(id=id, name=name)
