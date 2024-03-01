from enum import Enum

from ...bots.server_manager.srvm_autocompletes import FileAutocomplete, NotelistAutocomplete, NoteAutocomplete, ChannelTypeAutocomplete, DistantServerAutocomplete, TaskAutocomplete, IntervalUnitAutocomplete, PlaylistAutocomplete

class Autocompletes(Enum):
    file_autocomplete = FileAutocomplete
    notelist_autocomplete = NotelistAutocomplete
    note_autocomplete = NoteAutocomplete
    channel_type_autocomplete = ChannelTypeAutocomplete
    distant_server_autocomplete = DistantServerAutocomplete
    task_autocomplete = TaskAutocomplete
    interval_unit_autocomplete = IntervalUnitAutocomplete
    playlist_autocomplete = PlaylistAutocomplete