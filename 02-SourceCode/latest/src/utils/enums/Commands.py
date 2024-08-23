from enum import Enum

from ...bots.server_manager.srvm_commands import Setup, Help, Add, AddFile, AddNote, AddDistantServer, AddMusicToPlaylist, Create, CreateNoteList, CreateSpecialChannel, CreatePlaylist, Get, GetFile, GetNoteList, GetPlaylist, Delete, DeleteFile, DeleteNote, DeleteNoteList, DeleteDistantServer, Modify, ModifyNote, Start, StartTasks, Stop, StopTasks, Pv, ClosePrivateChannel, OpenPrivateChannel

class Commands(Enum):
    setup = Setup
    help = Help
    add = Add
    add_file = AddFile
    add_note = AddNote
    add_distant_server = AddDistantServer
    add_music_to_playlist = AddMusicToPlaylist
    create = Create
    create_note_list = CreateNoteList
    create_special_channel = CreateSpecialChannel
    create_playlist = CreatePlaylist
    get = Get
    get_file = GetFile
    get_note_list = GetNoteList
    get_playlist = GetPlaylist
    delete = Delete
    delete_file = DeleteFile
    delete_note = DeleteNote
    delete_note_list = DeleteNoteList
    delete_distant_server = DeleteDistantServer
    modify = Modify
    modify_note = ModifyNote
    start = Start
    start_tasks = StartTasks
    stop = Stop
    stop_tasks = StopTasks
    pv = Pv
    pv_close = ClosePrivateChannel
    pv_open = OpenPrivateChannel
