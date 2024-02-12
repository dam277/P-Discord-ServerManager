from enum import Enum

from ...bots.server_manager.srvm_commands import Setup, Help, Add, AddFile, AddNote, AddDistantServer, Create, CreateNoteList, CreateSpecialChannel, Get, GetFile, GetNoteList, Delete, DeleteFile, DeleteNote, DeleteNoteList, DeleteDistantServer, Modify, ModifyNote, Start, StartTasks, Stop, StopTasks

class Commands(Enum):
    setup = Setup
    help = Help
    add = Add
    add_file = AddFile
    add_note = AddNote
    add_distant_server = AddDistantServer
    create = Create
    create_note_list = CreateNoteList
    create_special_channel = CreateSpecialChannel
    get = Get
    get_file = GetFile
    get_note_list = GetNoteList
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