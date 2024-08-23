import json

class Command:
    """ # Command class
        
    Description :
    ---
        Manage commands as a parent of all of them

    Access : 
    ---
        src.bots.server_manager.commands.Command.py\n
        Command
    """
    def __init__(self):
        """ # Command class constructor
        
        Description :
        ---
            Construct a base command and get the setting as a self variable
        
        Access : 
        ---
            src.bots.commands.Command.py\n
            Command

        Returns : 
        ---
            :class:`None`
        """
        s = open("src/resources/configs/settings.json")
        self.settings = json.load(s)