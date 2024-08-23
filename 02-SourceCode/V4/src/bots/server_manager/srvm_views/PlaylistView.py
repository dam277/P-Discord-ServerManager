from time import sleep
import nextcord
import os
import ffmpeg
from .SelectorView import SelectorView

from ....database.models.srvm_tables.files.Music import Music

from ..._views.View import View

class PlaylistView(nextcord.ui.View, View):
    """ # PlaylistView class
    
    Description :
    ---
        Class for the playlist view
        
    Access :
    ---
        src.bots.server_manager.srvm_views.playlistView.py\n
        PlaylistView

    inheritance :
    ---
        - View : :class:`View` => Parent class of page views
    """
    def __init__(self, musics: list[Music], embed: nextcord.Embed):
        """ # PlaylistView constructor
        
        Description :
        ---
            Construct a PlaylistView object
        
        Access :
        ---
            src.bots.server_manager.srvm_views.playlistView.py\n
            PlaylistView.__init__()
        
        Parameters :
        ---
            - musics : :class:`Queue` => Queue of musics
            - embed : :class:`nextcord.Embed` => Embed of the playlist
        
        Returns :
        ---
            :class:`None`
        """
        super().__init__()
        super(View).__init__()

        self.embed = embed
        self.musics = musics
        self.current = 0
        self.is_playing = False
        self.time = 0

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji="⏮️")
    async def previous(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """ Previous button
        /!\\ This is a coroutine, it needs to be awaited

        Description :
        ---
            Go to the previous page

        Access :
        ---
            src.bots.server_manager.srvm_views.playlistView.py\n
            PlaylistView.previous()

        Parameters :
        ---
            - button : :class:`nextcord.ui.Button` => Button object
            - interaction : :class:`nextcord.Interaction` => Discord interaction object

        Returns :
        ---
            :class:`None`
        """
        await self.change_music(interaction, False)

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, emoji="▶️")
    async def play(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """ Play button
        /!\\ This is a coroutine, it needs to be awaited

        Description :
        ---
            Play the music

        Access :
        ---
            src.bots.server_manager.srvm_views.playlistView.py\n
            PlaylistView.play()

        Parameters :
        ---
            - button : :class:`nextcord.ui.Button` => Button object
            - interaction : :class:`nextcord.Interaction` => Discord interaction object

        Returns :
        ---
            :class:`None`
        """
        # Set the playing to True
        self.is_playing = True

        # Check if the bot is currently in a vocal channel
        if interaction.guild.voice_client is None:
            # Send a select box to select a vocal channel
            selector_view = SelectorView(options=[{"id": channel.id, "name": channel.name} for channel in interaction.guild.voice_channels], placeholder="Select a vocal channel")
            await interaction.channel.send("Select a vocal channel to play the music", view=selector_view)
            await selector_view.wait()
            self.time = 0

        # Connect to the vocal channel
        if interaction.guild.voice_client.is_paused():
            interaction.guild.voice_client.resume()

        # Start the loop for the time and play the current music
        while(self.is_playing):
            # Play the music on the vocal channel if the time is to 0
            if self.time == 1:
                interaction.guild.voice_client.play(nextcord.FFmpegPCMAudio(source=self.musics[self.current].path))

            # Check if the music is finished
            if self.time >= self.duration:
                await self.change_music(interaction, True)

            # Get the time
            self.time += 1
            t = self.get_precise_time(self.time)
            sleep(1) # 1 second

            # Modify the embed with the new time
            self.embed.remove_field(1)
            self.embed.add_field(name="", value=f"Time : {t}/{self.music_duration}", inline=False)
            await interaction.message.edit(embed=self.embed, view=self)

    @nextcord.ui.button(style=nextcord.ButtonStyle.grey, emoji="⏸️")
    async def pause(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """ Pause button
        /!\\ This is a coroutine, it needs to be awaited

        Description :
        ---
            Pause the music

        Access :
        ---
            src.bots.server_manager.srvm_views.playlistView.py\n
            PlaylistView.pause()

        Parameters :
        ---
            - button : :class:`nextcord.ui.Button` => Button object
            - interaction : :class:`nextcord.Interaction` => Discord interaction object

        Returns :
        ---
            :class:`None`
        """
        # Set the playing to False and pause the voice
        self.is_playing = False
        if interaction.guild.voice_client:
            interaction.guild.voice_client.pause()

    @nextcord.ui.button(style=nextcord.ButtonStyle.red, emoji="⏹️")
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """ stop button
        /!\\ This is a coroutine, it needs to be awaited

        Description :
        ---
            stop the music

        Access :
        ---
            src.bots.server_manager.srvm_views.playlistView.py\n
            PlaylistView.stop()

        Parameters :
        ---
            - button : :class:`nextcord.ui.Button` => Button object
            - interaction : :class:`nextcord.Interaction` => Discord interaction object

        Returns :
        ---
            :class:`None`
        """
        # Set the playing to False, stop the voice and disconnect the bot
        self.is_playing = False
        if interaction.guild.voice_client and interaction.guild.voice_client.is_connected():
            interaction.guild.voice_client.stop()
            await interaction.guild.voice_client.disconnect()

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji="⏭️")
    async def next(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """ Next button
        /!\\ This is a coroutine, it needs to be awaited

        Description :
        ---
            Go to the next page

        Access :
        ---
            src.bots.server_manager.srvm_views.playlistView.py\n
            PlaylistView.next()

        Parameters :
        ---
            - button : :class:`nextcord.ui.Button` => Button object
            - interaction : :class:`nextcord.Interaction` => Discord interaction object

        Returns :
        ---
            :class:`None`
        """
        await self.change_music(interaction, True)

    async def change_music(self, interaction: nextcord.Interaction, next: bool):
        """ # Change music function 
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Change the music
            
        Access :
        ---
            src.bots.server_manager.srvm_views.playlistView.py\n
            PlaylistView.change_music()
            
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Discord interaction object
            - next : :class:`bool` => Next music or previous music
        
        Returns :
        ---
            :class:`None`
        """        
        # Reset the time and stop the voice
        self.time = 0
        if interaction.guild.voice_client:
            interaction.guild.voice_client.stop()

        # Change the music
        if next and self.current < len(self.musics) - 1:
            self.current += 1
            await self.execute(interaction)
        elif not next and self.current > 0:
            self.current -= 1
            await self.execute(interaction)
        elif next and self.current == len(self.musics) - 1:
            self.current = 0
            await self.execute(interaction)
        elif not next and self.current == 0:
            self.current = len(self.musics) - 1
            await self.execute(interaction)

    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute function
        /!\\ This is a coroutine, it needs to be awaited

        Description :
        ---
            Execute the view

        Access :
        ---
            src.bots.server_manager.srvm_views.playlistView.py\n
            PlaylistView.execute()

        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Discord interaction object

        Returns :
        ---
            :class:`None`
        """
        # Get the actual file
        current_music = self.musics[self.current]
        
        # Check if the file exists
        if os.path.exists(current_music.path):
            # Get the time of the music
            self.duration = int(ffmpeg.probe(current_music.path)['format']['duration'].split(".")[0]) + 1
            self.music_duration = self.get_precise_time(self.duration)
        
        # Modify the embed with the new music
        self.embed.set_footer(text=f"Music {self.current + 1}/{len(self.musics)}")
        self.embed.clear_fields()
        self.embed.add_field(name="Title", value=current_music.name, inline=False)
        self.embed.add_field(name="", value=f"Time : 00:00/{self.music_duration}", inline=False)

        # Edit the message with the new embed
        if interaction.message:
            await interaction.message.edit(embed=self.embed, view=self)
