import nextcord
import os

from ...._views.ConfirmationView import ConfirmationView
from ...._commands.Command import Command

from .....database.models.tables.Server import Server

from .....utils.logger.Logger import Logger, LogDefinitions

class AddFile(Command):
    """ # AddFile command class 

    Description :
    ---
        Manage the AddFile discord command

    Access : 
    ---
        src.bots.server_manager.srvm_commands.files.AddFile.py\n
        AddFile

    inheritance : 
    ---
        - Command : :class:`Command` => Parent class of database commands
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

    async def execute(self, interaction: nextcord.Interaction):
        """ # Execute command function
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the command and make all connections with models and frontend (discord chat)
        
        Access : 
        ---
            src.bots.server_manager.srvm_commands.files.AddFile.py\n
            AddFile.execute()

        Parameters : 
        ---
            - interaction: :class:`nextcord.Interaction` => Interaction within the user and the command

        Returns : 
        ---
            :class:`None`
        """
        Logger.log(LogDefinitions.INFO, f"{__class__.__name__} command executed in guild {interaction.user.name}")

        # Create the confirmation view
        confirmation_view = ConfirmationView()

        # Check if the file is too big
        if self.file.size > self.settings["resources"]["max_file_size"]:
            # Ask the user to confirm or cancel the file upload
            await interaction.send('The file is too big to be send back to you (Maximum 25mo), do you still want to send this file ?', view=confirmation_view)
            await confirmation_view.wait()  # Wait for the user to make his choice
        
        # Get the server by guild_id and check if it exists in database
        server_id = await Server.get_server_id_by_guild_id(self.guild_id)
        if server_id is None:
            await interaction.followup.send("The server does not exists in database... Make a /setup first") if interaction.response.is_done() else await interaction.send("The server does not exists in database... Make a /setup first")
            Logger.log(LogDefinitions.WARNING, f"Server {self.guild_id} does not exists in database")
            return
        
        # Check if the user confirmed the file upload (pass if the file is smaller than max_file_size)
        if confirmation_view.value:
            # Set the paths for the file
            dir_path = f"{self.settings["resources"]["filesPath"]}/{self.guild_id}"
            file_path = f"{dir_path}/{self.file.filename}"

            # Create the directory if it doesn't exist
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            # Save the file
            await self.file.save(file_path)

            # Get the file type
            self.get_file_type(self.file.filename)

            # Save the file to the database
            message = await self.file_type.value.add_file(name=self.file.filename, path=file_path, fk_server=server_id)
            await interaction.followup.send(message) if interaction.response.is_done() else await interaction.send(message)
        else:
            # Cancel the file upload
            await interaction.followup.send("File upload canceled")
