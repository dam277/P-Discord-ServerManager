from ..Base import Base
import nextcord

from colorama import Fore
import copy

import asyncio

from ...utils.enums.permissions.DiscordPermissions import DiscordPermissions
from ...utils.enums.permissions.CheckType import CheckType

from ...utils.logger.Logger import Logger, LogDefinitions

class Event(Base):
    """ # Event class
    
    Description :
    ---
        Manage events as a parent of all of them
        
    Access :
    ---
        src.bots.server_manager.events.Event.py\n
        Event
    
    inheritance :
    ---
        - Base : :class:`Base` => Parent class of all commands
    """

    def trigger(name: str, parent: bool = False):
        """ # Trigger decorator

        Description :
        ---
            Decorate a function to be a trigger

        Access :
        ---
            src.bots.server_manager.events.Event.py\n
            Event.trigger()

        Parameters :
        ---
            - name : :class:`str` => Name of the event
        
        Returns :
        ---
            :class:`function`
        """
        def decorator(func):
            """ # Trigger decorator
            
            Description :
            ---
                Decorate a function to be a trigger
                
            Access :
            ---
                src.bots.server_manager.events.Event.py\n
                Event.trigger()
            
            Parameters :
            ---
                - func : :class:`function` => Function to decorate
                
            Returns :
            ---
                :class:`function`
            """
            def wrapper(self: Event, *args, **kwargs):
                """ # Trigger wrapper 

                Description :
                ---
                    Wrapper of the trigger decorator

                Access :
                ---
                    src.bots.server_manager.events.Event.py\n
                    Event.trigger().wrapper()

                Parameters :
                ---
                    - self : :class:`Event` => Event object
                    - *args : :class:`list` => Positional arguments
                    - **kwargs : :class:`dict` => Keyword arguments

                Returns :
                ---
                    :class:`function`
                """
                message = f"{name} event triggered"
                if parent:
                    message = f" -> {message}"
                Logger.log(LogDefinitions.INFO, message)
                return func(self, *args, **kwargs)
            return wrapper
        return decorator