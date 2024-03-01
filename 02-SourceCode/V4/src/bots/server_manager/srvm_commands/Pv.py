from operator import contains
import nextcord

from ....utils.enums.permissions.DiscordPermissions import DiscordPermissions

from ..._commands.Command import Command

class Pv(Command):
    """ # Pv command 
    
    Description :
    ---
        Pv a file to the server
    
    Access :
    ---
        src.bots.server_manager.bot_commands.Pv.py\n
        Pv
    
    Inheritence :
    ---
        :class:`Command`
    """

    def __init__(self):
        """ # Pv command constructor

        Description :
        ---
            Construct a Pv command object
        
        Access : 
        ---
            src.bots.server_manager.bot_commands.Pv.py\n
            Pv.__init__()

        Parameters :
        ---
            - guild_id : :class:`int` => Guild id of the command
            - file : :class:`nextcord.Attachment` => File to Pv

        Returns : 
        ---
            :class:`None`
        """
        super().__init__()

    @Command.register(name="/Pv", description="Manage private channels \n /!\\ This is a parent command which permit to use other subcommand by passing her")
    async def execute(self, interaction: nextcord.Interaction, *args, **kwargs):
        """ # Pv command execute method
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the Pv command
        
        Access :
        ---
            src.bots.server_manager.bot_commands.Pv.py\n
            Pv.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Interaction of the command
        
        Returns :
        ---
            :class:`None`
        """
        # Get the category where the command is executed
        self.category = interaction.channel.category

        # Check if there is a category and a private category
        if not self.category or not self.category.name.startswith(self.settings["resources"]["private_category_prefix"]):
            self.has_permission = False
            return await interaction.response.send_message("You can only use this command in a private channel", ephemeral=True)
        
        # Check if the user has the permission to use the command
        if not contains(self.category.name, interaction.user.name):
            self.has_permission = False
            return await interaction.response.send_message("You are not allowed to use this command here", ephemeral=True)
        
        return

