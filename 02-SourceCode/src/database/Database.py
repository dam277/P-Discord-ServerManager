import mysql.connector as connector
import os
import dotenv

from ..modules.logger import Logger as lg

class Database:
    """ Database class that manage the database interactions """
    instance = None
    def __init__(self):
        dotenv.load_dotenv()
        configs = {"db_host": os.getenv("DB_HOST"), "db_port": os.getenv("DB_PORT"), "db_user": os.getenv("DB_USER"), "db_password" : os.getenv("DB_PASSWORD"), "db_name": os.getenv("DB_NAME")}
        
        try:
            self.connection = connector.connect(host=configs["db_host"], port=configs["db_port"], user=configs["db_user"], passwd=configs["db_password"], database=configs["db_name"], autocommit=True)
            self.cursor = self.connection.cursor()
            lg.Logger.log(lg.LogDefinitions.SUCCESS, f"connected to the database")
        except Exception as e:
            lg.Logger.log(lg.LogDefinitions.ERROR, f"Exception while connecting to database : {e}")

    @staticmethod
    def get_instance():
        """ Get the instance of the Database and create a new if doesn't exist
        Return Database.instance : instance of the Database
        """
        if Database.instance is None:
            Database.instance = Database()
        return Database.instance
    
    async def bind_exec(self, query, values):
        """ Bind a query with values to avoid SQL injection 
        $param query: string -> SQL query to execute to the database
        $param values: dict -> Dictionnary of real values 
        Return self.cursor: MySqlCursor -> Request result """
        try:
            self.cursor.execute(query, values) 
            return self.cursor, True
        except connector.Error as err:
            lg.Logger.log(lg.LogDefinitions.ERROR, f"Exception while using database : {err}")
            return err, False
    
    async def simple_exec(self, query):
        """ Execute a simple query without binding parameters 
        $param query: string -> SQL query to execute to the database """
        self.cursor.execute(query)