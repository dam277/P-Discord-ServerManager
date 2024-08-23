from mysql.connector.cursor import MySQLCursor
from ...Database import Database
from ..Table import Table

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
        self.id = id
        self.channelID = channelID
        self.fk_server = fk_server

    @staticmethod
    async def get_channel_by_guild_id(server_id: int) -> "PrivateChannel":
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
        where = "fk_server = %(fk_server)s"
        query = f"SELECT * FROM {PrivateChannel.TABLE} WHERE {where};"

        # Get the result by executing query into the database
        result = await Database.get_instance().bind_exec(query, {"fk_server": server_id})
        if result[1] is True:
            return PrivateChannel.format_object(result)
        else:
            return result[0]
        
    @staticmethod
    async def get_channel_by_channel_id(channel_id: int) -> "PrivateChannel":
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

        # Get the result by executing query into the database
        result = await Database.get_instance().bind_exec(query, {"id_channel": channel_id})
        if result[1] is True:
            return PrivateChannel.format_object(result)
        else:
            return result[0]
        
    @staticmethod
    async def create_channel(channel_id: int, server_id: int) -> "PrivateChannel":
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
        params = "(%(id_privateChannel)s, %(fk_server)s, %(channelID)s)"
        query = f"INSERT INTO {PrivateChannel.TABLE} {fields} VALUES {params};"

        # Get the result by executing query into the database
        result = await Database.get_instance().bind_exec(query, {"id_privateChannel" : None, "fk_server": server_id, "channelID": channel_id})
        if result[1] is True:
            return PrivateChannel.format_object(result)
        else:
            return result[0]
        
    @staticmethod 
    async def delete_channel_by_id(channel_id: int) -> str:
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

        # Get the result by executing query into the database
        result = await Database.get_instance().bind_exec(query, {"channelID": channel_id})
        if result[1] is True:
            return f"The channel has been successfully deleted from the database"
        else:
            return result[0]
        
    @staticmethod
    def format_object(cursor_result: MySQLCursor) -> "PrivateChannel":
        """ # Format object function
        @staticmethod
        
        Description :
        ---
            Format a :class:`PrivateChannel` object by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.PrivateChannel.py\n
            PrivateChannel.format_object()

        Parameters : 
        ---
            - cursor_result : :class:`MySQLCursor` => Result of the query

        Returns : 
        ---
            :class:`PrivateChannel|None` => A PrivateChannel object
        """
        # Getting datas from result
        row = PrivateChannel.get_one_row(cursor_result[0])

        # Check if datas are filled
        if row is None or len(row) < 1:
            return None
        
        # Get the datas from the row
        private_channel = PrivateChannel.create_object(row)
        return private_channel
    
    @staticmethod
    def format_list_object(cursor_result: MySQLCursor) -> list["PrivateChannel"]:
        """ # Format list object function
        @staticmethod
        
        Description :
        ---
            Format a :class:`PrivateChannel` object list by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.PrivateChannel.py\n
            PrivateChannel.format_list_object()

        Parameters : 
        ---
            - cursor_result : :class:`MySQLCursor` => Result of the query

        Returns : 
        ---
            :class:`list[PrivateChannel]|None` => A list of PrivateChannel object
        """
        # Getting datas from result
        rows = PrivateChannel.get_all_rows(cursor_result[0])
        
        # Check if datas are filled
        if len(rows) < 1:
            return None
        
        # List all the PrivateChannels
        private_channels = []
        for row in rows:
            # Create a PrivateChannel object and return it
            private_channel = PrivateChannel.create_object(row)
            private_channels.append(private_channel)

        return private_channels
    
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
        private_channel = PrivateChannel(id=row[0], fk_server=row[1], channelID=row[2])
        return private_channel