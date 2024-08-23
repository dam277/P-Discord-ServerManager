from ..Base import Base
import nextcord

from colorama import Fore
import copy

import asyncio

from ...utils.enums.permissions.DiscordPermissions import DiscordPermissions
from ...utils.enums.permissions.CheckType import CheckType

from ...utils.logger.Logger import Logger, LogDefinitions

class View(Base):
    """ # View class
    
    Description :
    ---
        Manage views as a parent of all of them
        
    Access :
    ---
        src.bots.server_manager.views.View.py\n
        View
    
    inheritance :
    ---
        - Base : :class:`Base` => Parent class of all commands
    """

    
