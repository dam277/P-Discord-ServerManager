from enum import Enum

from ...database.models.srvm_tables.files.Music import Music
from ...database.models.srvm_tables.files.Image import Image
from ...database.models.srvm_tables.File import File

class FileTypes(Enum):
    IMAGE = Image
    MUSIC = Music
    DEFAULT = File

class FileTypesString(Enum):
    IMAGE = "img"
    MUSIC = "mus"
    DEFAULT = ""