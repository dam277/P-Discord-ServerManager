import nextcord
import os

#from ..srvm_views.ConfirmationView import ConfirmationView
from ....._commands.Command import Command

from ....._events.Event import Event
from ......database.models.tables.Server import Server
from ......database.models.tables.PrivateChannel import PrivateChannel

from ......utils.logger.Logger import Logger, LogDefinitions
from ......utils.enums.CommandContext import CommandContext

class OnVoiceStateUpdate(Event):
    """ # OnVoiceStateUpdate event class

    Description :
    ---
        Manage the OnVoiceStateUpdate event discord event

    Access :
    ---
        src.bots.server_manager.srvm_events.OnVoiceStateUpdate.py\n
        OnVoiceStateUpdate

    inheritance :
    ---
        - Event : :class:`Event` => Parent class of all events
    """
    def __init__(self, member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState):
        """ # OnVoiceStateUpdate constructor

        Description :
        ---
            Construct a ChannelEvents object

        Access :
        ---
            src.bots.server_manager.srvm_events.ChannelEvents.py\n
            ChannelEvents.__init__()

        Returns :
        ---
            :class:`None`
        """
        self.member = member
        self.before = before
        self.after = after
        super().__init__()

    @Event.trigger(name="on_voice_state_update")
    async def execute(self):
        """ # OnVoiceStateUpdate event execute method

        Description :
        ---
            Execute the OnVoiceStateUpdate event

        Access :
        ---
            src.bots.server_manager.srvm_events.OnVoiceStateUpdate.py\n
            OnVoiceStateUpdate.on_guild_channel_delete()

        Returns :
        ---
            :class:`None`
        """
        # Check if the user did change his channel state
        if self.after.channel != self.before.channel:
            # Check if the user joined, left or switched channel
            if self.after.channel is not None:
                await self.on_voice_channel_join()

            if self.before.channel is not None:
                await self.on_voice_channel_leave()

    @Event.trigger(name="on_voice_channel_join", parent=True)
    async def on_voice_channel_join(self):
        """ # OnVoiceStateUpdate event on_voice_channel_join method

        Description :
        ---
            Execute the OnVoiceStateUpdate event when a member join a voice channel

        Access :
        ---
            src.bots.server_manager.srvm_events.OnVoiceStateUpdate.py\n
            OnVoiceStateUpdate.on_voice_channel_join()

        Returns :
        ---
            :class:`None`
        """
        Logger.log(LogDefinitions.INFO, f"{self.member.name} joined the channel {self.after.channel.name}")
        
        # Get the guild
        guild = self.after.channel.guild
        
        # Check if the channel is the private channel
        private_channel_result = await PrivateChannel.get_channel_by_channel_id(self.after.channel.id)

        async def create_private_category():
            """ # Create private category function
            
            Description :
            ---
                Create a private category for the user
            
            Access :
            ---
                src.bots.server_manager.srvm_events.OnVoiceStateUpdate.py\n
                OnVoiceStateUpdate.on_voice_channel_join.create_private_category()
                
            Returns :
            ---
                :class:`None`
            """
            # Create a new category for the user
            Logger.log(LogDefinitions.INFO, f"Create a new category for {self.member.name}")
            category_name = f"{self.settings["resources"]["private_category_prefix"]}-{self.member.name}"
            
            # Create the category
            category = await guild.create_category(category_name)

            # Add permissions to the category to let only the user see and join it
            await category.set_permissions(guild.default_role, view_channel=False)
            await category.set_permissions(self.member, view_channel=True)
            
            # Get the commands
            commands = [command for command in Command.get_commands() if command.get("context") == CommandContext.PRIVATECHANNEL]
            
            # Create the channels into the category
            general = await guild.create_text_channel("general", category=category)

            # Send the commands in the general channel if there is any
            if len(commands) > 0:
                # Create an embed to display the commands
                embed = nextcord.Embed(title="Commands", description="Here is the list of commands you can use in this channel", color=0x00ff00)
                for command in commands:
                    # Get the params of the command
                    params = command.get("params")
                    command_description = f"{command.get("description")}\n\t**Parameters :**"

                    # Get the params of the command
                    for param in params:
                        param_description = params.get(param)
                        # Check if the param contains "[optional]"
                        if "[optional]" in param_description:
                            # Remove "[optional]" from the param description and put it before the param name
                            param_description = param_description.replace("[optional]", "")
                            command_description += f"\n- _**[optional]** {param} : {param_description}_"
                        else:
                            command_description += f"\n- {param} : {param_description}"

                    embed.add_field(name=command.get("name"), value=command_description, inline=False)
                await general.send(embed=embed)

            voice = await guild.create_voice_channel("voice", category=category)

            # Move the user to the voice channel
            await self.member.move_to(voice)

        # Check if the channel exists and if this is the private channel
        if private_channel_result.get("passed") and private_channel_result.get("object") is not None and private_channel_result.get("object").channelID == self.after.channel.id:
            await create_private_category()
    
    @Event.trigger(name="on_voice_channel_leave", parent=True)
    async def on_voice_channel_leave(self):
        """ # OnVoiceStateUpdate event on_voice_channel_leave method

        Description :
        ---
            Execute the OnVoiceStateUpdate event when a member leave a voice channel

        Access :
        ---
            src.bots.server_manager.srvm_events.OnVoiceStateUpdate.py\n
            OnVoiceStateUpdate.on_voice_channel_leave()

        Returns :
        ---
            :class:`None`
        """
        Logger.log(LogDefinitions.INFO, f"{self.member.name} left the channel {self.before.channel.name}")
        
        # Get the guild
        guild = self.before.channel.guild
        category = self.before.channel.category

        # Check if the channel is on a private category and the category name contains the owner member name
        if self.before.channel.category is not None and self.before.channel.category.name.startswith(self.settings["resources"]["private_category_prefix"]) and self.member.name in self.before.channel.category.name:
            await self.delete_category(category)
    