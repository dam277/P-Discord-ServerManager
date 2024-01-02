import logging
from dotenv import load_dotenv
import os

from src.bots.server_manager.ServerManagerBot import ServerManagerBot

def main():
    """ # Main function
        
    Description :
    ---
        Entry point of the program

    Access : 
    ---
        main.py\n
        main()

    Return :
    ---
        :class:`None`
    """
    # Set the config of logging and load dotenv
    #logging.basicConfig(filename="logs.log", filemode="w", level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    load_dotenv()

    # Create a server manager bot
    server_manager_token = os.getenv("BOT_SERVER_MANAGER_TOKEN")
    server_manager_bot = ServerManagerBot(server_manager_token)
    server_manager_bot.run()

if __name__ == '__main__':
    main()
    