import nextcord

from ....._commands.Command import Command
from ...Pv import Pv

class ClosePrivateChannel(Pv):
    """ # ClosePrivateChannel command

    Description :
    ---
        Close a private channel

    Access :
    ---
        src.bots.server_manager.srvm_commands.channels.private.ClosePrivateChannel.py\n
        ClosePrivateChannel

    Inheritence :
    ---
        :class:`Pv`
    """

    def __init__(self, user: nextcord.User):
        """ # ClosePrivateChannel command constructor

        Description :
        ---
            Construct a ClosePrivateChannel command object

        Access :
        ---
            src.bots.server_manager.srvm_commands.channels.private.ClosePrivateChannel.py\n
            ClosePrivateChannel.__init__()

        Parameters :
        ---
            - guild_id : :class:`int` => Guild id of the command
            - channel : :class:`nextcord.Channel` => Channel to close

        Returns :
        ---
            :class:`None`
        """
        self.user = user
        super().__init__()

    @Command.register(name="pv_close", description="Close a private channel", parent="/Pv", user="THe user to close the private channel for")
    async def execute(self, interaction: nextcord.Interaction):
        """ # ClosePrivateChannel command execute method
        /!\\ This is a coroutine, it needs to be awaited

        Description :
        ---
            Execute the ClosePrivateChannel command

        Access :
        ---
            src.bots.server_manager.srvm_commands.channels.private.ClosePrivateChannel.py\n
            ClosePrivateChannel.execute()

        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => The interaction object
            - args : :class:`list` => List of arguments
            - kwargs : :class:`dict` => Dictionary of keyword arguments

        Returns :
        ---
            :class:`None`
        """
        await super().execute(interaction)
        if not self.has_permission:
            return
        
        # Change the permissions of the category
        await self.category.set_permissions(self.user, view_channel=False)

        # Send a confirmation message
        await interaction.send(f"Private channel closed for {self.user.name}")

        