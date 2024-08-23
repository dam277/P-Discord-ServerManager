import nextcord
import os

from ...._autocompletes.Autocomplete import Autocomplete

from .....database.models.tables.Server import Server
from .....database.models.tables.Note import Note

class NoteAutocomplete(Autocomplete):
    """ # NoteAutocomplete autocomplete class
    
    Description :
    ---
        Manage the NoteAutocomplete discord autocomplete
        
    Access :
    ---
        src.bots.server_manager.srvm_autocompletes.notes.NoteAutocomplete.py\n
        NoteAutocomplete
        
    inheritance :
    ---
        - autocomplete : :class:`autocomplete` => Parent class of database autocompletes"""
    def __init__(self, current: str, guild_id: int):
        """ # NoteAutocomplete autocomplete constructor
        
        Description :
        ---
            Construct a NoteAutocomplete autocomplete object
            
        Access :
        ---
            src.bots.server_manager.srvm_autocompletes.notes.NoteAutocomplete.py\n
            NoteAutocomplete.__init__()
        
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
            src.bots.server_manager.srvm_autocompletes.notes.NoteAutocomplete.py\n
            NoteAutocomplete.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Nextcord interaction object
            
        Returns :
        ---
            :class:`None`
        """
        # Get the server id
        server_id_result = await Server.get_server_id_by_guild_id(self.guild_id)

        # Check if the server exists
        if server_id_result.get("value"):
            # Get the notelists
            notes_result = await Note.get_notes_in_notelists_by_server_id(server_id_result.get("value"))
            
            # Execute the autocomplete
            await super().execute(interaction, notes_result.get("objects"), "title")
            return
        
        # Send empty autocomplete
        await interaction.response.send_autocomplete([])