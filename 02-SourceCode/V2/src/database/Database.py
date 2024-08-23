import mysql.connector as connector
from mysql.connector.cursor import MySQLCursor
import os
import dotenv

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
    def __init__(self):
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
        dotenv.load_dotenv()
        configs = {"db_host": os.getenv("DB_HOST"), "db_port": os.getenv("DB_PORT"), "db_user": os.getenv("DB_USER"), "db_password" : os.getenv("DB_PASSWORD"), "db_name": os.getenv("DB_NAME")}
        
        # Try to connect the database server
        try:
            self.connection = connector.connect(host=configs["db_host"], port=configs["db_port"], user=configs["db_user"], passwd=configs["db_password"], database=configs["db_name"], autocommit=True)
            self.cursor = self.connection.cursor()
            Logger.log(LogDefinitions.SUCCESS, f"connected to the database")
        except Exception as e:
            Logger.log(LogDefinitions.ERROR, f"Exception while connecting to database : {e}")

    @staticmethod
    def get_instance():
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
            Database.instance = Database()
        return Database.instance
    
    async def bind_exec(self, query, values) -> tuple[MySQLCursor|str, bool]:
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
            return self.cursor, True
        except connector.Error as err:
            Logger.log(LogDefinitions.ERROR, f"Exception while using database binded execute : {err}")
            return err.msg, False
    
    async def simple_exec(self, query) -> tuple[MySQLCursor|str, bool]:
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
            return self.cursor, True
        except connector.Error as err:
            Logger.log(LogDefinitions.ERROR, f"Exception while using database simple execute : {err}")
            return err.msg, False