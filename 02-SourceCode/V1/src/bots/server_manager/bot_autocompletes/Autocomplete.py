class Autocomplete:
    """ # Autocomplete base class

    Description :
    ---
        Manage the discord autocompletes

    Access :
    ---
        src.bots.server_manager.autocompletes.Autocomplete.py\n
        Autocomplete

    inheritance :
    ---
        - object : :class:`object` => Python object class
    """
    def __init__(self, current: str):
        """ # Autocomplete base constructor

        Description :
        ---
            Construct a Autocomplete object

        Access :
        ---
            src.bots.server_manager.autocompletes.Autocomplete.py\n
            Autocomplete.__init__()

        Returns :
        ---
            :class:`None`
        """
        self.current = current