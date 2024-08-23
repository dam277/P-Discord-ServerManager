import nextcord
import os

from ...._autocompletes.Autocomplete import Autocomplete

from .....database.models.tables.Server import Server
from .....database.models.tables.File import File

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
        server_id = await Server.get_server_id_by_guild_id(self.guild_id)

        # Get and Filter the files by checking the name of the file and make that the result max length is 25
        files = await File.get_files_by_server_id(server_id)
        if files:
            files = [f.name for f in files if self.current.lower() in f.name.lower()][:25]
        else:
            files = []
            
        # Send the autocomplete response
        await interaction.response.send_autocomplete(files)
