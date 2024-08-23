from src.database.models.tables.Server import Server    
from src.database.models.tables.File import File    
from src.database.models.tables.Note import Note    
from src.database.models.tables.NoteList import NoteList  
from src.database.models.tables.PrivateChannel import PrivateChannel  
import asyncio


async def main():
    tesdt  =1
    # srv_result = await Server.get_all_servers()

    # if srv_result.get("passed"):
    #     servers = srv_result.get("objects")
    #     for server in servers:
    #         print(server.name)
    # else:
    #     print(srv_result.get("error"))

    # result = await Server.create_server(123456789, "test")

    # if result.get("passed"): 
    #     print("passed")
    # else:
    #     print(result.get("error"))

    # srv_result = await Server.get_server_id_by_guild_id(123456789)

    # if srv_result.get("passed"):
    #     srv = srv_result.get("values")
    #     print(srv)
    # else:
    #     print(srv_result.get("error"))

    # note_list_result = await NoteList.get_all_note_lists()

    # if note_list_result.get("passed"):
    #     note_lists = note_list_result.get("objects")
    #     print(note_lists[0].name)

    # if note_list_result.get("passed"):
    #     note_list = note_list_result.get("value")
    #     print(note_list)

    # if file_result.get("passed"):
    #     files = file_result.get("objects")
    #     for file in files:
    #         print(file.path)
    # else:
    #     print(file_result.get("error"))

    # private_channel_result = await PrivateChannel.get_channel_by_guild_id(817075041501446154)

    # if private_channel_result.get("passed"):
    #     private_channel = private_channel_result.get("object")
    #     print(private_channel.id)
    # else:
    #     print(private_channel_result.get("error"))

    srv_res = await Server.get_server_by_guild_id(817075041501446154)

asyncio.run(main())