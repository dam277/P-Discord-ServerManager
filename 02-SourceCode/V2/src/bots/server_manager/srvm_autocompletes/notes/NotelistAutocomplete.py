import nextcord
import os

from ...._autocompletes.Autocomplete import Autocomplete

from .....database.models.tables.Server import Server
from .....database.models.tables.NoteList import NoteList

class NotelistAutocomplete(Autocomplete):
    """ # NotelistAutocomplete autocomplete class
    
    Description :
    ---
        Manage the NotelistAutocomplete discord autocomplete
        
    Access :
    ---
        src.bots.server_manager.srvm_autocompletes.notes.NotelistAutocomplete.py\n
        NotelistAutocomplete
        
    inheritance :
    ---
        - autocomplete : :class:`autocomplete` => Parent class of database autocompletes"""
    def __init__(self, current: str, guild_id: int):
        """ # NotelistAutocomplete autocomplete constructor
        
        Description :
        ---
            Construct a NotelistAutocomplete autocomplete object
            
        Access :
        ---
            src.bots.server_manager.srvm_autocompletes.notes.NotelistAutocomplete.py\n
            NotelistAutocomplete.__init__()
        
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
            src.bots.server_manager.srvm_autocompletes.notes.NotelistAutocomplete.py\n
            NotelistAutocomplete.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Discord interaction with the user
            
        Returns :
        ---
            :class:`None`
        """
        # Get the server id
        id_server = await Server.get_server_id_by_guild_id(self.guild_id)

        # Get the notelists
        notelists = await NoteList.get_notelists_by_server_id(id_server)
        print(notelists)

        if notelists:
            notelists = [notelist.name for notelist in notelists if self.current.lower() in notelist.name.lower()][:25]
        else:
            notelists = []

        # Send the autocomplete response
        await interaction.response.send_autocomplete(notelists)