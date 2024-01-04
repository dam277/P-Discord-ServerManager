import nextcord
from nextcord.ext import commands

from ...._commands.Command import Command

from .....utils.logger.Logger import Logger, LogDefinitions

class GetCommands(Command):
    """ # GetCommands command class 
        
    Description :
    ---
        Manage the Get commands discord command

    Access : 
    ---
        src.bots.server_manager.srvm_commands.help.GetCommands.py\n
        GetCommands

    inheritance : 
    ---
        - Command : :class:`Command` => Parent class of database commands
    """
    def __init__(self, slash_commands: set[nextcord.BaseApplicationCommand], regular_commands: set[commands.Command]):
        """ # GetCommands command constructor

        Description :
        ---
            Construct a GetCommands command object
        
        Access : 
        ---
            src.bots.server_manager.srvm_commands.help.GetCommands.py\n
            GetCommands.__init_()

        Parameters : 
        ---
            - commands : :class:`set` => commands of the bot

        Returns : 
        ---
            :class:`None`
        """
        self.slash_commands = slash_commands
        self.regular_commands = regular_commands
        super().__init__()

    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute command function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the command and make all connections with models and frontend (discord chat)
        
        Access : 
        ---
            src.bots.server_manager.bot_commands.help.GetCommands.py\n
            GetCommands.execute()

        Parameters : 
        ---
            - interaction: :class:`nextcord.Interaction` => Interaction within the user and the command

        Returns : 
        ---
            :class:`None`
        """
        Logger.log(LogDefinitions.INFO, f"DeleteFile command called by {interaction.user.name}")
        
        # Get the bot's commands
        self.embedMessage = nextcord.Embed(title="Bot commands", description="Here are all the commands of the bot that can be used!")

        # Set the commands into the embed message
        self.set_embed_slash_commands()
        self.set_embed_regular_commands()

        # Reply with an embed of all commands
        await interaction.send(embed=self.embedMessage, ephemeral=True)

    def set_embed_slash_commands(self):
        """ # Set embed slash commands function
        
        Description :
        ---
            Set the slash commands into an embed object with their options
        
        Access : 
        ---
            src.bots.server_manager.bot_commands.help.GetCommands.py\n
            GetCommands.set_embed_slash_commands()

        Returns : 
        ---
            :class:`None`
        """
        # Get slash commands
        for command in self.slash_commands:
            # Get command options
            command_params = ""
            for param in command.options:
                command_params += f"<{param} : [{getattr(type(param), "__name__", "")}]>"

            # Get the subcommands
            subcommands = ""
            subcommands_descriptions = ""
            if command.get_payload(None).get("options", None):
                for subcommand in command.get_payload(None).get("options", None):
                    subcommands += f"|{subcommand.get("name")}|"
                    subcommands_descriptions += f"{subcommand.get("name")} : {subcommand.get("description")} \n"

            # Set a new field for a new command
            self.embedMessage.add_field(name=f"/{command.name} {command_params} {subcommands}", value=command.description, inline=False)
            self.embedMessage.add_field(name="- Subcommands", value=subcommands_descriptions, inline=False) if subcommands != "" else None

    def set_embed_regular_commands(self):
        """ # Set embed regular commands function
        
        Description :
        ---
            Set the regular commands into an embed object with their options
        
        Access : 
        ---
            src.bots.server_manager.bot_commands.help.GetCommands.py\n
            GetCommands.set_embed_regular_commands()

        Returns : 
        ---
            :class:`None`
        """
        # Get regular commands
        for command in self.regular_commands:
            # Get command params
            command_params = ""
            for param in command.params:
                # Check if not ctx as param and add it to the string
                if not "ctx" in param:
                    command_params += f"<{param} : [{getattr(type(param), "__name__", "")}]> "

            # Set a new field for a new command
            self.embedMessage.add_field(name=f"${command.name} {command_params}", value=command.description, inline=False)