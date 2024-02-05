from enum import Enum

from ...bots.server_manager.srvm_autocompletes import FileAutocomplete, NotelistAutocomplete, NoteAutocomplete, ChannelTypeAutocomplete

class Autocompletes(Enum):
    file_autocomplete = FileAutocomplete
    notelist_autocomplete = NotelistAutocomplete
    note_autocomplete = NoteAutocomplete
    channel_type_autocomplete = ChannelTypeAutocomplete