import nextcord
import os

from ...._autocompletes.Autocomplete import Autocomplete

from .....database.models.tables.Server import Server
from .....database.models.tables.File import File
from .....database.models.tables.files.Image import Image
from .....database.models.tables.files.Music import Music

from .....utils.logger.Logger import Logger, LogDefinitions
from .....utils.enums.FileTypes import FileTypesString

class FileAutocomplete(Autocomplete):
    """ # FileAutocomplete autocomplete class
    
    Description :
    ---
        Manage the FileAutocomplete discord autocomplete
        
    Access :
    ---
        src.bots.server_manager.srvm_autocomplete.files.AutocompleteFile.py\n
        AutocompleteFile
        
    inheritance :
    ---
        - autocomplete : :class:`autocomplete` => Parent class of database autocompletes"""
    def __init__(self, current: str, guild_id: int):
        """ # FileAutocomplete autocomplete constructor
        
        Description :
        ---
            Construct a FileAutocomplete autocomplete object
            
        Access :
        ---
            src.bots.server_manager.srvm_autocomplete.files.AutocompleteFile.py\n
            AutocompleteFile.__init__()
        
        Parameters :
        ---
            - current : :class:`str` => Current string of the autocomplete
            - guild_id : :class:`int` => Guild id of the autocomplete
            
        Returns :
        ---
            :class:`None`
        """
        self.guild_id = guild_id

        super().__init__(current)

    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute autocomplete function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the autocomplete and make all connections with models and frontend (discord chat)       
            
        Access :
        ---
            src.bots.server_manager.srvm_autocomplete.files.AutocompleteFile.py\n
            AutocompleteFile.execute()
            
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Interaction within the user and the autocomplete
        
        Returns :
        ---
            :class:`None`
        """
        # Get the server id
        server_id_result = await Server.get_server_id_by_guild_id(self.guild_id)
        
        # Check if the server exists
        if server_id_result.get("value"):
            request = File.get_files_by_server_id

            # Check the extension of the file depending on the current string
            if self.current.startswith(f"$-{FileTypesString.IMAGE.value}"):
                self.current = self.current.replace(f"$-{FileTypesString.IMAGE.value}", "").replace(" ", "")
                request = Image.get_images_by_server_id
            elif self.current.startswith(f"$-{FileTypesString.MUSIC.value}"):
                self.current = self.current.replace(f"$-{FileTypesString.MUSIC.value}", "").replace(" ", "")
                request = Music.get_musics_by_server_id

            # Get the files
            files_result = await request(server_id_result.get("value"))
            
            # Execute the autocomplete
            await super().execute(interaction, files_result.get("objects"), "name")
            return
        
        # Send empty autocomplete
        await interaction.response.send_autocomplete([])