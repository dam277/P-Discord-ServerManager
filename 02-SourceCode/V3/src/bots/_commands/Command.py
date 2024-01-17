from ..Base import Base
import nextcord

from ...utils.enums.permissions.DiscordPermissions import DiscordPermissions
from ...utils.enums.permissions.CheckType import CheckType

from ...utils.logger.Logger import Logger, LogDefinitions

class Command(Base):
    """ # Command class
        
    Description :
    ---
        Manage commands as a parent of all of them

    Access : 
    ---
        src.bots.server_manager.commands.Command.py\n
        Command

    inheritance :
    ---
        - Base : :class:`Base` => Parent class of all commands
    """
    commands = []

    # Permision decorator
    def permissions(perms: list[DiscordPermissions], check_type: CheckType = CheckType.any):
        """ # Permission decorator
        @Decorator
        
        Description :
        ---
            Check if the user has the perms to execute the command
        
        Access :
        ---
            src.bots.server_manager.commands.Command.py\n
            @Command.permissions()
        
        Parameters :
        ---
            - perms : :class:`list` => Perms to check
            - check_type : :class:`CheckType` => Type of the check
        
        Returns :
        ---
            :class:`None`
        """
        # Decorator function
        def decorator(func):
            # Check if the perms sended are valid
            invalid_perms = set(perm.value for perm in perms) - set(nextcord.Permissions.VALID_FLAGS)
            if invalid_perms:
                Logger.log(LogDefinitions.ERROR, f"invalid permission(s) sended: {', '.join(invalid_perms)}")

            # Wrapper function
            def wrapper(object: object, interaction: nextcord.Interaction):
                Logger.log(LogDefinitions.INFO, "Checking permission...")

                # Get the channel and the permissions of the user
                channel = interaction.channel
                permissions = channel.permissions_for(interaction.user)

                # Check if the user has the perms
                passed = False

                # Check if the user has one of the perms or all of them
                if check_type == CheckType.any:
                    # Check if the user has one of the perms
                    boolean_perms = [getattr(permissions, perm.value) for perm in perms]
                    if True in boolean_perms:
                        passed = True
                else:
                    # Get the missing permissions by comparing the perms sended and the perms of the user for the actual channel and check if the user has all the perms
                    missing_perms = [perm.value for perm in perms if not getattr(permissions, perm.value)]
                    if not missing_perms:
                        passed = True

                # Check if the user has the perms
                if passed:
                    # Execute the original command function
                    Logger.log(LogDefinitions.INFO ,"Permission granted for the command")
                    return func(object, interaction)
                else:
                    # Send a message to the user to tell him he doesn't have the permission to execute the command
                    Logger.log(LogDefinitions.WARNING ,"Permission denied for the command")
                    return Base.permission_denied(interaction)
            return wrapper
        return decorator

    # Register command decorator
    def register(name: str, description: str, parent: str = None, **params):
        """ # Register command decorator
        @Decorator

        Description :
        ---
            Register a command in the commands list

        Access :
        ---
            src.bots.server_manager.commands.Command.py\n
            @Command.register()

        Parameters :
        ---
            - name : :class:`str` => Name of the command
            - description : :class:`str` => Description of the command
            - parent : :class:`str` => Parent of the command
            - params : :class:`dict` => Params of the command

        Returns :
        ---
            :class:`None`
        """
        # Register the command
        Logger.log(LogDefinitions.INFO ,f"Registering command: '{name}'")

        # Check if the command name and description are valid
        if not name or not description:
            Logger.log(LogDefinitions.ERROR ,f"Invalid command name or description")
            
        # Register the command
        command = {"name": name, "description": description, "parent": parent, "params": params}
        Command.commands.append(command)

        # Check if the command has been successfully registered 
        if not command in Command.commands:
            Logger.log(LogDefinitions.ERROR ,f"Error while registering command: '{name}'")
        Logger.log(LogDefinitions.SUCCESS ,f"Command registered as: '{name}' with params : {params}")
        
        # Decorator function
        def decorator(func):
            # Wrapper function
            def wrapper(*args, **kwargs):
                # Execute the original command function
                Logger.log(LogDefinitions.INFO ,f"Executing command: '{name}'")
                result = func(*args, **kwargs)
                Logger.log(LogDefinitions.INFO ,f"Command execution complete.")
                return result
            return wrapper
        return decorator
    
    # Get commands function
    @staticmethod
    def get_commands() -> list[dict]:
        """ # Get commands function
        
        Description :
        ---
            Get all the commands registered in the bot

        Access : 
        ---
            src.bots.server_manager.commands.Command.py\n
            Command.get_commands()

        Parameters :
        ---
            None

        Returns : 
        ---
            :class:`list` => List of all the commands registered in the bot
        """
        return Command.commands
    
    # Get command function
    @staticmethod
    def get_command(name: str) -> dict:
        """ # Get command function
        
        Description :
        ---
            Get a command by his name

        Access : 
        ---
            src.bots.server_manager.commands.Command.py\n
            Command.get_command()

        Parameters :
        ---
            name : :class:`str` => Name of the command to get

        Returns : 
        ---
            :class:`Command` => Command with the name sended
        """
        return next((command for command in Command.commands if command.get("name") == name), None)
    
    # Get command by parent function
    @staticmethod
    def get_ordered_commands() -> list[dict]:
        """ # Get ordered commands function

        Description :
        ---
            Get a command by his parent

        Access : 
        ---
            src.bots.server_manager.commands.Command.py\n
            Command.get_command_by_parent()

        Parameters :
        ---
            parent : :class:`str` => Parent of the command to get

        Returns : 
        ---
            :class:`Command` => Command with the parent sended
        """
        # Get all the top and children commands
        top_commands = [command for command in Command.commands if not command.get("parent")]
        children_commands = [command for command in Command.commands if command.get("parent")]

        # Get children function with recursivity
        def get_children(command: dict):
            """ # Get children function
            
            Description :
            ---
                Get the children of a command with recursivity
            
            Access :
            ---
                src.bots.server_manager.commands.Command.py\n
                Command.get_children()
                
            Parameters :
            ---
                command : :class:`dict` => Command to get the children
                
            Returns :
            ---
                :class:`dict` => Command with the children
            """
            # Get all the subcommands of the actual command
            subcommands = [subcommand for subcommand in children_commands if subcommand.get("parent") == command.get("name")]

            # For all the subcommands of the actual command get their children
            for subcommand in subcommands:
                # Check if the command has children
                if not command.get("children"):
                    # If not, create a children list to add his children into it
                    command.update({"children": []})

                # Add the children to the children list while calling the function again to get them
                command.get("children").append(get_children(subcommand))

            # Return the command (the first command to be returned, is the most down command in the children tree that the recursivity will return)
            # After that, the command which will be returned will be the parent of the previous command with his children as a list
            return command
        
        # Get all the commands with their children
        commands = []
        for command in top_commands:
            commands.append(get_children(command))

        # Return the commands
        return commands