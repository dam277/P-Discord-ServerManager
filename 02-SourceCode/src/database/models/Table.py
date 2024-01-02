from mysql.connector.cursor import MySQLCursor 

class Table:
    """ # Table class
        
    Description :
    ---
        Generic class for all the tables of the database

    Access : 
    ---
        src.database.models.Table.py
        
        Table
    """
    @staticmethod
    def get_one_row(cursor: MySQLCursor) -> tuple:
        """ # Get one row subfunction
        @staticmethod

        Description :
        ---
            Fetch one row of the passed msql cursor element and returns it
        
        Access : 
        ---
            src.database.models.Table.py\n
            Table.get_one_row()

        Parameters : 
        ---
            - cursor : :class:`MySQLCursor` => result of the query

        Returns : 
        ---
            :class:`tuple`|:class:`None` => One row of result
        """
        return cursor.fetchone()
    
    @staticmethod
    def get_all_rows(cursor: MySQLCursor) -> list:
        """ # Get one row subfunction
        @staticmethod
        
        Description :
        ---
            Fetch all rows of the passed msql cursor element and returns it
        
        Access : 
        ---
            src.database.models.Table.py\n
            Table.get_all_rows()

        Parameters : 
        ---
            - cursor : :class:`MySQLCursor` => result of the query

        Returns : 
        ---
            :class:`list` => All rows of result
        """
        return cursor.fetchall()