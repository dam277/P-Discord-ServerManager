from enum import Enum

from ...bots.server_manager.srvm_commands import Setup, Help

class Commands(Enum):
    setup = Setup
    help = Help