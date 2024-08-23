import nextcord

from ....._commands.Command import Command
from ...Pv import Pv

class OpenPrivateChannel(Pv):
    """ # OpenPrivateChannel command

    Description :
    ---
        Close a private channel

    Access :
    ---
        src.bots.server_manager.srvm_commands.channels.private.OpenPrivateChannel.py\n
        OpenPrivateChannel

    Inheritence :
    ---
        :class:`Pv`
    """

    def __init__(self, user: nextcord.User):
        """ # OpenPrivateChannel command constructor

        Description :
        ---
            Construct a OpenPrivateChannel command object

        Access :
        ---
            src.bots.server_manager.srvm_commands.channels.private.OpenPrivateChannel.py\n
            OpenPrivateChannel.__init__()

        Returns :
        ---
            :class:`None`
        """
        self.user = user
        super().__init__()

    @Command.register(name="pv_open", description="Open a private channel", parent="/Pv", user="THe user to open the private channel for")
    async def execute(self, interaction: nextcord.Interaction):
        """ # OpenPrivateChannel command execute method
        /!\\ This is a coroutine, it needs to be awaited

        Description :
        ---
            Execute the OpenPrivateChannel command

        Access :
        ---
            src.bots.server_manager.srvm_commands.channels.private.OpenPrivateChannel.py\n
            OpenPrivateChannel.execute()

        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => The interaction object

        Returns :
        ---
            :class:`None`
        """
        await super().execute(interaction)
        if not self.has_permission:
            return
        
        # Change the permissions of the category
        await self.category.set_permissions(self.user, view_channel=True)

        # Send a confirmation message
        await interaction.send(f"Private channel opened for {self.user.name}")