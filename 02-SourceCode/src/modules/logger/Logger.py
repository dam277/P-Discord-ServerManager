from colorama import Fore
import logging

from enum import Enum

class LogDefinitions(Enum):
    MESSAGE = 0
    DEBUG = 1
    SUCCESS = 2
    INFO = 3
    WARNING = 4
    ERROR = 5
    CRITICAL = 6

class Logger:
    @staticmethod
    def log(definition, message):
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