import nextcord

import threading

from .....utils.enums.permissions.DiscordPermissions import DiscordPermissions

from .....utils.enums.Tasks import Tasks

from ..Stop import Stop
from ...._commands.Command import Command

class StopTasks(Stop):
    """ # StopTasks command class
    
    Description :
    ---
        Manage the StopTasks command discord command
    
    Access :
    ---
        src.bots.server_manager.srvm_commands.tasks.StopTasks.py\n
        StopTasks
    
    inheritance :
    ---
        - stop : :class:`stop` => Parent class of tasks commands
    """
    def __init__(self, guild: nextcord.Guild, task_name: str|None):
        """ # StopTasks command constructor
        
        Description :
        ---
            Construct a StopTasks command object
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.tasks.StopTasks.py\n
            StopTasks.__init__()
        
        Parameters :
        ---
            - task : :class:`Tasks` => Task to stop
            - guild_id : :class:`int` => Guild id of the command
            
        Returns :
        ---
            :class:`None`
        """
        self.guild = guild
        self.task_name = task_name

        super().__init__()

    @Command.permissions([DiscordPermissions.administrator])
    @Command.register(name="stop_tasks", description="stop all the tasks of the bot", parent="/stop", task_name="[optional]name of the task to stop")
    async def execute(self, interaction: nextcord.Interaction, *args, **kwargs):
        """ # StopTasks command execute method
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the StopTasks command
        
        Access :
        ---
            src.bots.server_manager.srvm_commands.tasks.StopTasks.py\n
            StopTasks.execute()
        
        Parameters :
        ---
            - interaction : :class:`nextcord.Interaction`
        
        Returns :
        ---
            :class:`None`
        """
        # Execute the parent function
        await super().execute(interaction)
        if not self.has_permission:
            return   
                
        # stop all the tasks
        for task in Tasks:
            # Get the task class and the task list
            task_class = task.value.get("class")
            task_list = task_class.tasks_list
            task_code_name = f"{self.guild.id}-{task.value.get('name')}"

            # Check if the task exists
            if not task_list.get(task_code_name):
                continue

            # Check if the task is a specific task
            task_code_name = f"{self.guild.id}-{self.task_name}" if self.task_name else task_code_name
            print(task_code_name)
            # Check if the task is running
            if task_list.get(task_code_name) and task_list.get(task_code_name).execute.is_running():
                print("Task is running so we stop it")
                task_list.get(task_code_name).stop()

        # Send the response
        return await interaction.send(f"{task.value.get('name')} Task stopped") if self.task_name else await interaction.send("All tasks stopped")


            


            

