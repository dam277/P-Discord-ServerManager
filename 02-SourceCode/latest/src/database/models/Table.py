from mysql.connector.cursor import MySQLCursor 
from typing import Union

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
    def __init__(self, id):
        """ # Class constructor of Table object

        Description :
        ---
            Construct a Table object with parameters passed to use it more easily

        Access :
        ---
            src.database.models.Table.py\n
            Table.__init__()
        
        Parameters :
        ---
            - id : :class:`int` => Id of the Table
        
        Returns :
        ---
            :class:`None`
        """
        self.id = id    
    
    @staticmethod
    def format_object(cursor: MySQLCursor, create_object_func: classmethod, uniquely_values = False) -> dict[bool, Union["Table", dict]]:
        """ # Format object function
        @staticmethod
        
        Description :
        ---
            Format a :class:`obj` object by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.obj.py\n
            obj.format_object()

        Parameters : 
        ---
            - cursor : :class:`MySQLCursor` => Result of the query

        Returns : 
        ---
            :class:`obj|None` => A obj object
        """
        # Getting datas from result
        cursor_row = cursor.fetchone()

        # Check if datas are filled if not return None
        if cursor_row is None or len(cursor_row) < 1:
            return {"passed" : True, "object" : None}
        
        # Create a dict with the datas
        row = dict(zip(cursor.column_names, cursor_row))
        
        # Check if we want to return the values uniquely
        if uniquely_values:
            # Check if there is only one value
            if len(row) == 1:
                return {"passed" : True, "value" : row.popitem()[1]}
            return {"passed" : True, "values" : row}
        
        # Create a full object and returns it
        obj = create_object_func(row)
        return {"passed" : True, "object" : obj}
    
    @staticmethod
    def format_list_object(cursor: MySQLCursor, create_object_func: classmethod, uniquely_values: bool = False, can_be_none: bool = False ) -> dict[bool, list[Union["Table", dict]]]:
        """ # Format list object function
        @staticmethod
        
        Description :
        ---
            Format a :class:`obj` object list by recieving a database cursor execution result
        
        Access : 
        ---
            src.database.models.tables.Server.py\n
            Server.format_list_object()

        Parameters : 
        ---
            - cursor : :class:`MySQLCursor` => Result of the query

        Returns : 
        ---
            :class:`list[Server]|None` => A list of Server object
        """
        # Getting datas from result
        rows = []
        for row in cursor.fetchall():
            rows.append(dict(zip(cursor.column_names, row)))
        
        # Check if datas are filled
        if len(rows) < 1 and not can_be_none:
            return {"passed" : False, "objects" : None}
        elif len(rows) < 1 and can_be_none:
            return {"passed" : True, "values" : rows}
        
        if uniquely_values:
            # Check if there is only one value
            if len(rows[0]) == 1:
                return {"passed" : True, "values" : [row.popitem()[1] for row in rows]}
            return {"passed" : True, "values" : rows}

        # List all the objs
        objs = []
        for row in rows:
            # Create a server object and add it to the objs list
            obj = create_object_func(row)
            objs.append(obj)

        return {"passed" : True, "objects" : objs}