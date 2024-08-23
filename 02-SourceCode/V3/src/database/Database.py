import mysql.connector as connector
from mysql.connector.cursor import MySQLCursor

from ..utils.logger.Logger import Logger, LogDefinitions

class Database:
    """ # Database class
        
    Description :
    ---
        Database class that manage the database server interactions 

    Access : 
    ---
        src.database.Database.py\n
        Database
    """
    instance = None         # Instance of the database
    def __init__(self, configs: dict[str, str] = None):
        """ # Class constructor of database
        
        Description :
        ---
            Construct a database instance to connect to the database server using the dotenv 
        
        Access : 
        ---
            src.database.Database.py\n
            Database.__init__()

        Returns : 
        ---
            :class:`None`

        Raises : 
        ---
            :class:`Exception`
            :class:`DatabaseConnectionExeption`
        """
        # Get the datas to connect the server
        self.configs = configs
        
        # Try to connect the database server
        try:
            self.connection = connector.connect(host=configs["db_host"], port=configs["db_port"], user=configs["db_user"], passwd=configs["db_password"], database=configs["db_name"], autocommit=True)
            self.cursor = self.connection.cursor()
            Logger.log(LogDefinitions.SUCCESS, f"connected to the database")
        except Exception as e:
            Logger.log(LogDefinitions.ERROR, f"Exception while connecting to database : {e}")

    @staticmethod
    def get_instance(configs: dict[str, str] = None):
        """ # get_instance function
        @staticmethod
        
        Description :
        ---
            Get the instance of the Database and create a new if doesn't exist
        
        Access : 
        ---
            src.database.Database.py\n
            Database.get_instance()

        Returns : 
        ---
            :class:`Database.instance` => instance of the Database
        """
        # Create a new instance if doesn't exist
        if Database.instance is None:
            Database.instance = Database(configs)
        return Database.instance
    
    async def bind_exec(self, query, values) -> dict[bool, MySQLCursor|str]:
        """ # Bind database execution
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Bind a query with values to avoid SQL injection
        
        Access : 
        ---
            src.database.Database.py\n
            Database.bind_exec()

        Parameters : 
        ---
            - query : :class:`str` => SQL query to execute to the database
            - values : :class:`dict` => Dictionnary of real values 

        Returns : 
        ---
            self.cursor : :class:`MySqlCursor` => Request result

        Raises : 
        ---
            :class:`conector.Error`
        """
        try:
            self.cursor.execute(query, values) 
            return {"passed" : True, "cursor" : self.cursor}
        except connector.Error as err:
            Logger.log(LogDefinitions.ERROR, f"Exception while using database binded execute : {err}")
            return {"passed" : False, "error" : err.msg}
    
    async def simple_exec(self, query) -> dict[bool, MySQLCursor|str]:
        """ # Simple database execution
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute a simple query without binding parameters 
        
        Access : 
        ---
            src.database.Database.py\n
            Database.simple_exec()

        Parameters : 
        ---
            - query : :class:`str` => SQL query to execute to the database

        Returns : 
        ---
            self.cursor : :class:`MySqlCursor` => Request result

        Raises : 
        ---
            :class:`conector.Error`
        """
        try:
            self.cursor.execute(query)
            return {"passed" : True, "cursor" : self.cursor}
        except connector.Error as err:
            Logger.log(LogDefinitions.ERROR, f"Exception while using database simple execute : {err}")
            return {"passed" : False, "error" : err.msg}