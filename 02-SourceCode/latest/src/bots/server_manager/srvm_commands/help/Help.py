import nextcord

from ...._commands.Command import Command

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
    
    @Command.register(name="/help", description="Show the help message and get the list of usable commands")
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
        discord_commands = Command.get_ordered_commands()
        embed = nextcord.Embed(title="Help", description="Here is the list of all the commands", color=0x00ff00)

        # Get children function with recursivity
        def set_embed(command: dict, depth: int = 1):
            """ # Set embed function

            Description :
            ---
                Set the embed with the commands wit recursivity

            Access :
            ---
                src.bots.server_manager.srvm_commands.help.Help.py\n
                Help.execute(set_embed())
            
            Parameters :
            ---
                - command : :class:`dict` => Command to set
                - depth : :class:`int` => Depth of the command
            
            Returns :
            ---
                :class:`None`
            """
            # Get all the subcommands of the actual command
            subcommands = command.get("children") if command.get("children") else None
            # Check if the command has children
            if subcommands:
                # For all the subcommands of the actual command get their children
                for subcommand in subcommands:

                    # Create the name of the function with depth => "-" and command name
                    command_name = f"{'-' * depth} [{depth}] {subcommand.get("name")}"
                    command_description = f"{subcommand.get("description")}"
                    
                    # Get the params of the subcommand
                    params = subcommand.get("params")
                    if params:
                        command_description += "\n\t**Parameters :**"

                        # Get the params of the subcommand
                        for param in params:
                            param_description = params.get(param)
                            # Check if the param contains "[optional]"
                            if "[optional]" in param_description:
                                # Remove "[optional]" from the param description and put it before the param name
                                param_description = param_description.replace("[optional]", "")
                                command_description += f"\n- \_**[optional]** {param} : {param_description}"
                            else:
                                command_description += f"\n- {param} : {param_description}"

                    # Add the subcommand to the embed
                    embed.add_field(name=f"__{command_name}__", value=command_description, inline=False)
                    set_embed(subcommand, depth + 1)

        # For all the commands get their children and add them to the embed
        for command in discord_commands:
            embed.add_field(name=command.get("name"), value=command.get("description"), inline=False)
            set_embed(command)

        # Send the embed to the user
        await interaction.response.send_message(embed=embed, ephemeral=True)
