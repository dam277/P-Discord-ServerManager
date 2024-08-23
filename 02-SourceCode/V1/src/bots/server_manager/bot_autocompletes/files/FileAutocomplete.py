import nextcord
import os

from .....database.models.tables.Server import Server
from .....database.models.tables.File import File
from ..Autocomplete import Autocomplete
from .....database.models.tables.Server import Server
from .....database.models.tables.File import File


class FileAutocomplete(Autocomplete):
    """ # FileAutocomplete command class
    
    Description :
    ---
        Manage the FileAutocomplete discord command
        
    Access :
    ---
        src.bots.server_manager.bot_autocomplete.files.AutocompleteFile.py\n
        AutocompleteFile
        
    inheritance :
    ---
        - Command : :class:`Command` => Parent class of database commands"""
    def __init__(self, current, guild_id):
        """ # FileAutocomplete command constructor
        
        Description :
        ---
            Construct a FileAutocomplete command object
            
        Access :
        ---
            src.bots.server_manager.bot_autocomplete.files.AutocompleteFile.py\n
            AutocompleteFile.__init__()
        
        Parameters :
        ---
            - current : :class:`str` => Current string of the autocomplete
            - guild_id : :class:`int` => Guild id of the command
            
        Returns :
        ---
            :class:`None`
        """
        self.guild_id = guild_id

        super().__init__(current)

    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute command function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the command and make all connections with models and frontend (discord chat)       
            
        Access :
        ---
            src.bots.server_manager.bot_autocomplete.files.AutocompleteFile.py\n
            AutocompleteFile.execute()
            
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Interaction within the user and the command
        
        Returns :
        ---
            :class:`None`
        """
        # Get the server id
        server_id = await Server.get_server_id_by_guild_id(self.guild_id)

        # Get all the files of the server
        files = await File.get_files_by_server_id(server_id)

        # Filter the files by checking the name of the file
        if self.current:
            files = [f for f in files if self.current.lower() in f.name.lower()]

        # Get the 25 first files
        filtered_files = []
        for file in files:
            if len(filtered_files) < 25:
                filtered_files.append(file.name)

        # Send the autocomplete response
        await interaction.response.send_autocomplete(filtered_files)
