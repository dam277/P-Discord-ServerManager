from enum import Enum

from ...bots.server_manager.srvm_commands import Setup, Help, Add, AddFile, AddNote, CreateNoteList, CreatePrivateChannel

class Commands(Enum):
    setup = Setup
    help = Help
    add = Add
    add_file = AddFile
    add_note = AddNote
    create_note_list = CreateNoteList
    create_private_channel = CreatePrivateChannel