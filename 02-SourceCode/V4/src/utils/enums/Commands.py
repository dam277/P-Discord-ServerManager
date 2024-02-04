from enum import Enum

from ...bots.server_manager.srvm_commands import Setup, Help, Add, AddFile, AddNote, Create, CreateNoteList, CreatePrivateChannel, Get, GetFile, GetNoteList, Delete, DeleteFile, DeleteNote, DeleteNoteList, Modify, ModifyNote

class Commands(Enum):
    setup = Setup
    help = Help
    add = Add
    add_file = AddFile
    add_note = AddNote
    create = Create
    create_note_list = CreateNoteList
    create_private_channel = CreatePrivateChannel
    get = Get
    get_file = GetFile
    get_note_list = GetNoteList
    delete = Delete
    delete_file = DeleteFile
    delete_note = DeleteNote
    delete_note_list = DeleteNoteList
    modify = Modify
    modify_note = ModifyNote
