import nextcord
from ..._views.View import View

class SelectorView(nextcord.ui.View, View):
    """ # SelectorView class
    
    Description :
    ---
        Manage the selector view
        
    Access :
    ---
        src.bots._views.SelectorView.py\n
        SelectorView
    
    inheritance :
    ---
        - View : :class:`View` => Parent class of page views
    """
    def __init__(self, options: list[dict[str, str]], placeholder: str, min_values: int = 1, max_values: int = 1):
        """ # PageView constructor

        Description :
        ---
            Construct a PageView object

        Access :
        ---
            src.bots._views.PageView.py\n
            PageView.__init__()

        Parameters :
        ---
            - options : :class:`list` => List of options
            - placeholder : :class:`str` => Placeholder of the selector
            - min_values : :class:`int` => Minimum number of values
            - max_values : :class:`int` => Maximum number of values

        Returns :
        ---
            :class:`None`
        """
        super().__init__()
        super(View).__init__()

        self.options = options
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values

        self.dropdown = nextcord.ui.Select(placeholder=self.placeholder, options=[nextcord.SelectOption(label=option.get("name"), value=option.get("id")) for option in self.options], min_values=self.min_values, max_values=self.max_values)
        self.dropdown.callback = self.dropdown_callback
        self.add_item(self.dropdown)

    async def dropdown_callback(self, interaction: nextcord.Interaction):
        """ # Dropdown callback function

        Description :
        ---
            Callback function for the dropdown

        Access :
        ---
            src.bots._views.SelectorView.py\n
            SelectorView.dropdown_callback()

        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Discord interaction object

        Returns :
        ---
            :class:`None`
        """
        for value in self.dropdown.values:
            await interaction.guild.get_channel(int(value)).connect()

        self.stop()

    async def execute(self, interation: nextcord.Interaction):
        """ # SelectorView class execute method

        Description :
        ---
            Execute the SelectorView

        Access :
        ---
            src.bots.SelectorView.py\n
            SelectorView.execute()

        Parameters :
        ---
            interation : :class:`nextcord.Interaction`

        Returns :
        ---
            :class:`None`
        """
        pass