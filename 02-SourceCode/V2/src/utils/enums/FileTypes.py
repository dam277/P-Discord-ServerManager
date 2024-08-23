from enum import Enum

from ...database.models.tables.files.Music import Music
from ...database.models.tables.files.Image import Image
from ...database.models.tables.File import File

class FileTypes(Enum):
    IMAGE = Image
    MUSIC = Music
    DEFAULT = File
