from ..Base import Base
import nextcord

from ...utils.enums.permissions.DiscordPermissions import DiscordPermissions
from ...utils.enums.permissions.CheckType import CheckType
from ...utils.enums.Commands import Commands

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
    
    # Permision decorator
    def permissions(perms: list[DiscordPermissions], check_type: CheckType = CheckType.any):
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

    # Command decorator
    def command(command: Commands):
        def decorator(func):
            # Wrapper function
            def wrapper(*args, **kwargs):
                # Wrap the function and execute it
                Logger.log(LogDefinitions.INFO ,f"Executing command: '{command.value}'")
                result = func(*args, **kwargs)
                Logger.log(LogDefinitions.INFO ,f"Command execution complete.")
                return result
            return wrapper
        return decorator