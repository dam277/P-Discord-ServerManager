from mysql.connector.cursor import MySQLCursor 

class Table:
    """ Generic class for all the tables of the database """
    @staticmethod
    def get_one_row(cursor: MySQLCursor) -> tuple:
        """ Get one row from the msql cursor 
        $param cursor: MySQLCursor => result of the query """
        return cursor.fetchone()
    
    @staticmethod
    def get_all_rows(cursor: MySQLCursor) -> list:
        """ Get all rows from the msql cursor 
        $param cursor: MySQLCursor => result of the query """
        return cursor.fetchall()