import logging
from dotenv import load_dotenv
import os

from src.bots.server_manager.ServerManagerBot import ServerManagerBot

def main():
    logging.basicConfig(filename="logs.log", filemode="w", level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    load_dotenv()

    server_manager_token = os.getenv("BOT_SERVER_MANAGER_TOKEN")
    server_manager_bot = ServerManagerBot(server_manager_token)
    server_manager_bot.run()

if __name__ == '__main__':
    main()
    