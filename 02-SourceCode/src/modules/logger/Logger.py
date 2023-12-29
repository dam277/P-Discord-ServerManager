from colorama import Fore
import logging

from enum import Enum

class LogDefinitions(Enum):
    """ # Logger enum
        
    Description :
    ---
        Log definitions that defines the severity of the log that will be passed

    Access : 
    ---
        src.modules.logger.Logger.py\n
        LogDefinitions

    Inheritance : 
    ---
        :class:`Enum`
    """
    MESSAGE = 0
    DEBUG = 1
    SUCCESS = 2
    INFO = 3
    WARNING = 4
    ERROR = 5
    CRITICAL = 6

class Logger:
    """ # Logger class
        
    Description :
    ---
        Logger class of the program used to log informations in the terminal and a log file

    Access : 
    ---
        src.modules.logger.Logger.py\n
        Logger
    """
    @staticmethod
    def log(definition, message):
        """ # Log function
            
        Description :
        ---
            Display a log message on the terminal and a log file by passing the message and the log severity

        Access : 
        ---
            src.modules.logger.Logger.py\n
            Logger.log()

        Return :
        ---
            :class:`None`
        """
        match definition:
            case LogDefinitions.MESSAGE:
                print(f"{Fore.MAGENTA}-> {message} {Fore.RESET}")
            case LogDefinitions.DEBUG:
                print(f"{Fore.MAGENTA}DEBUG: {message} {Fore.RESET}")
            case LogDefinitions.SUCCESS:
                print(f"{Fore.GREEN}SUCCESS: {message} {Fore.RESET}")
                logging.info(f"Successfully {message}")
            case LogDefinitions.INFO:
                print(f"{Fore.BLUE}INFO: {message} {Fore.RESET}")
                logging.info(message)
            case LogDefinitions.WARNING:
                print(f"{Fore.YELLOW}WARNING: {message} {Fore.RESET}")
                logging.warning(message)
            case LogDefinitions.ERROR:
                print(f"{Fore.LIGHTRED_EX}ERROR: {message} {Fore.RESET}")
                logging.error(message)
            case LogDefinitions.CRITICAL:
                print(f"{Fore.RED}CRITICAL: {message} {Fore.RESET}")
                logging.critical(message)