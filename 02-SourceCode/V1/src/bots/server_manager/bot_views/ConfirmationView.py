import nextcord

class ConfirmationView(nextcord.ui.View):
    """ ConfirmationView class 

    Description :
    ---
        Manage the confirmation view

    Inheritance :
    ---
        - :class:`nextcord.ui.View`

    Access :
    ---
        src.bots.server_manager.bot_views.ConfirmationView.py\n
        ConfirmationView
    """
    def __init__(self):
        """ ConfirmationView constructor 

        Description :
        ---
            Construct a ConfirmationView object

        Access :
        ---
            src.bots.server_manager.bot_views.ConfirmationView.py\n
            ConfirmationView.__init__()

        Returns :
        ---
            :class:`None`        
        """
        super().__init__()
        self.value = True

    @nextcord.ui.button(label='Confirm', style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """ Confirm button
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Confirm a choice of the user
        
        Access :
        ---
            src.bots.server_manager.bot_views.ConfirmationView.py\n
            ConfirmationView.confirm()
        
        Parameters :
        ---
            - button : :class:`nextcord.ui.Button` => Button that was pressed
            - interaction : :class:`nextcord.Interaction` => Interaction with the user

        Returns :
        ---
            :class:`None`
        """
        self.value = True
        self.stop()

    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """ Cancel button 
        /!\\ This is a coroutine, it needs to be awaited

        Description :
        ---
            Cancel a choice of the user

        Access :
        ---
            src.bots.server_manager.bot_views.ConfirmationView.py\n
            ConfirmationView.cancel()
        
        Parameters :
        ---
            - button : :class:`nextcord.ui.Button` => Button that was pressed
            - interaction : :class:`nextcord.Interaction` => Interaction with the user

        Returns :
        ---
            :class:`None`
        """
        self.value = False
        self.stop()