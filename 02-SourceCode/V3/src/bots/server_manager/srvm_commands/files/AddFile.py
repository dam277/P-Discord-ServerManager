import nextcord
from nextcord.ext import commands
import os

from .....utils.enums.permissions.DiscordPermissions import DiscordPermissions

from ...._commands.Command import Command
from ..Add import Add
from ...srvm_views.ConfirmationView import ConfirmationView

from .....database.models.tables.Server import Server

from .....utils.logger.Logger import Logger, LogDefinitions

class AddFile(Add):
    """ # AddFile command 
    
    Description :
    ---
        Add a file to the server
    
    Access :
    ---
        src.bots.server_manager.bot_commands.files.AddFile.py\n
        AddFile
    
    Inheritence :
    ---
        :class:`Command`
    """

    def __init__(self, guild_id: int, file: nextcord.Attachment):
        """ # AddFile command constructor

        Description :
        ---
            Construct a AddFile command object
        
        Access : 
        ---
            src.bots.server_manager.srvm_commands.files.AddFile.py\n
            AddFile.__init__()

        Parameters :
        ---
            - guild_id : :class:`int` => Guild id of the command
            - file : :class:`nextcord.Attachment` => File to add

        Returns : 
        ---
            :class:`None`
        """
        self.guild_id = guild_id
        self.file = file
        super().__init__()

    @Command.register(name="add_file", description="Add a file to the server", parent="/add", file="File attachement which you want to add imported from your pc")
    async def execute(self, interaction: nextcord.Interaction):
        """ # AddFile command execute method

        Description :
        ---
            Execute the AddFile command
        
        Access : 
        ---
            src.bots.server_manager.srvm_commands.files.AddFile.py\n
            AddFile.execute()

        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction` => Interaction of the command

        Returns : 
        ---
            :class:`None`
        """
        # Execute the parent function
        await super().execute(interaction)
        if not self.has_permission:
            return

        # Create confirmation view
        confirmation_view = ConfirmationView()
        
        # Check if the file is to big
        if self.file.size > self.settings["resources"]["max_file_size"]:
            await confirmation_view.execute(interaction, "The file is too big, are you sure you want to upload it ?")
        
            # Check if the user confirmed
            if not confirmation_view.value:
                # Cancel the file upload
                return await interaction.followup.send("File upload canceled")
        
        # Get the server by guild_id
        server_datas = await Server.get_server_id_by_guild_id(self.guild_id)

        # Check if the query passed
        if not server_datas.get("passed"):
            Logger.log(LogDefinitions.ERROR, f"An error occured while getting the server id : {server_datas.get("error")}")
            return await interaction.followup.send(f"An error occured while getting the server id : {server_datas.get("error")}", ephemeral=True) if interaction.response.is_done() else await interaction.send(f"An error occured while getting the server id : {server_datas.get("error")}", ephemeral=True)

        # Check if the server exists in database
        if not server_datas.get("value"):
            Logger.log(LogDefinitions.WARNING, f"Server {self.guild_id} does not exists in database")
            return await interaction.followup.send("The server does not exists in database... Make a /setup first") if interaction.response.is_done() else await interaction.send("The server does not exists in database... Make a /setup first")
            
        # Get the server id
        server_id = server_datas.get("value")

        # Set the paths for the file
        dir_path = f"{self.settings["resources"]["filesPath"]}/{self.guild_id}"
        file_path = f"{dir_path}/{self.file.filename}"

        # Get the file type
        self.get_file_type(self.file.filename)

        # Check if the file already exists in database
        file_exists_result = await self.file_type.value.get_file_by_path(file_path)
        if not file_exists_result.get("passed"):
            Logger.log(LogDefinitions.ERROR, f"An error occured while getting the file : {file_exists_result.get("error")}")
            return await interaction.followup.send(f"An error occured : {file_exists_result.get("error")}", ephemeral=True) if interaction.response.is_done() else await interaction.send(f"An error occured : {file_exists_result.get("error")}", ephemeral=True)

        # Check if the file already exists
        if file_exists_result.get("object"):
            Logger.log(LogDefinitions.WARNING, f"File {self.file.filename} already exists")
            return await interaction.followup.send(f"File **{self.file.filename}** already exists") if interaction.response.is_done() else await interaction.send(f"File **{self.file.filename}** already exists")

        # Create the directory if it doesn't exist
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Save the file
        await self.file.save(file_path)

        # Save the file to the database
        result = await self.file_type.value.add_file(name=self.file.filename, path=file_path, fk_server=server_id)

        # Check if the query passed and send the message
        message = f"File **{self.file.filename}** added successfully"
        if not result.get("passed"):
            message = f"An error occured while adding the file : {result.get("error")}"
            Logger.log(LogDefinitions.ERROR, message)
        
        # Send the message
        return await interaction.followup.send(message) if interaction.response.is_done() else await interaction.send(message)