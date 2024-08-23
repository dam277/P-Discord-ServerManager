import nextcord

from ..._views.View import View

class ConfirmationView(nextcord.ui.View, View):
    """ ConfirmationView class

    Description :   
    ---
        Manage a confirmation view
    
    Inheritences :
    ---
        - value : :class:`View` => Value of the confirmation
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
        super(View).__init__()

        self.value = None

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

    async def execute(self, interaction: nextcord.Interaction, message: str):
        """ # ConfirmationView execute method

        Description :
        ---
            Execute the ConfirmationView

        Access :
        ---
            src.bots.server_manager.bot_views.ConfirmationView.py\n
            ConfirmationView.execute()

        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Interaction with the user

        Returns :
        ---
            :class:`None`
        """
        await interaction.response.send_message(message, view=self)
        await self.wait()