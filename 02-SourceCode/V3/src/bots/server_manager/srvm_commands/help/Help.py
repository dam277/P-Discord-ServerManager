import nextcord
from nextcord.ext import commands
from colorama import Fore

from .....utils.enums.permissions.DiscordPermissions import DiscordPermissions

from ...._commands.Command import Command

from .....database.models.tables.Server import Server

from .....utils.logger.Logger import Logger, LogDefinitions

class Help(Command):
    """ # Help command class
        
    Description :
    ---
        Class of a command that called "help"

    Access : 
    ---
        src.bots.server_manager.srvm_commands.help.Help.py\n
        Help

    inheritance : 
    ---
        - Command : :class:`Command` => Parent class of all commands
    """    
    def __init__(self):
        """ # Constructor of help command
        
        Description :
        ---
            Construct an object of :class:`Help`

        Access : 
        ---
            src.bots.server_manager.srvm_commands.help.Help.py\n
            Help.__init__

        Returns : 
        ---
            :class:`None`
        """
        # Set the datas into the parent
        super().__init__()
    
    @Command.register(name="/help", description="Show the help message with all the commands")
    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute method of help command
        
        Description :
        ---
            Execute the help command

        Access : 
        ---
            src.bots.server_manager.srvm_commands.help.Help.py\n
            Help.execute()

        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Interaction of the command

        Returns : 
        ---
            :class:`None`
        """
        print(Command.get_commands())
        discord_commands = Command.get_ordered_commands()
        embed = nextcord.Embed(title="Help", description="Here is the list of all the commands", color=0x00ff00)

        
        # Get children function with recursivity
        def set_embed(command: dict, depth: int = 1):
            # Get all the subcommands of the actual command
            subcommands = command.get("children") if command.get("children") else None
            print(f"{Fore.MAGENTA}Subcommands : of {command.get("name")}", subcommands)

            # Check if the command has children
            if subcommands:
                # For all the subcommands of the actual command get their children
                for subcommand in subcommands:
                    print(f"{Fore.LIGHTYELLOW_EX}Subcommand : {subcommand}")

                    # Create the name of the function with depth => "-" and command name
                    command_name = f"{'_' * depth} [{depth}] {subcommand.get("name")}"

                    # Add the subcommand to the embed
                    embed.add_field(name=command_name, value=subcommand.get("description"), inline=False)
                    set_embed(subcommand, depth + 1)

        for command in discord_commands:
            embed.add_field(name=command.get("name"), value=command.get("description"), inline=False)

            set_embed(command)

        await interaction.response.send_message(embed=embed, ephemeral=True)
