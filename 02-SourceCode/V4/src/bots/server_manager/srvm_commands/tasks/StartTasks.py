import nextcord

import threading

from .....utils.enums.permissions.DiscordPermissions import DiscordPermissions

from .....utils.enums.Tasks import Tasks

from ..Start import Start
from ...._commands.Command import Command

class StartTasks(Start):
    """ # StartTasks command class
    
    Description :
    ---
        Manage the StartTasks command discord command
    
    Access :
    ---
        src.bots.server_manager.srvm_commands.tasks.StartTasks.py\n
        StartTasks
    
    inheritance :
    ---
        - Start : :class:`Start` => Parent class of tasks commands
    """
    def __init__(self, guild: nextcord.Guild, task_name: str|None):
        """ # StartTasks command constructor
        
        Description :
        ---
            Construct a StartTasks command object
            
        Access :
        ---
            src.bots.server_manager.srvm_commands.tasks.StartTasks.py\n
            StartTasks.__init__()
        
        Parameters :
        ---
            - task : :class:`Tasks` => Task to start
            - guild_id : :class:`int` => Guild id of the command
            
        Returns :
        ---
            :class:`None`
        """
        self.guild = guild
        self.task_name = task_name

        super().__init__()

    @Command.permissions([DiscordPermissions.administrator])
    @Command.register(name="start_tasks", description="Start all the tasks of the bot", parent="/start", task_name="[optional]name of the task to start")
    async def execute(self, interaction: nextcord.Interaction, *args, **kwargs):
        """ # StartTasks command execute method
        /!\\ This is a coroutine, it needs to be awaited
        
        Description :
        ---
            Execute the StartTasks command
        
        Access :
        ---
            src.bots.server_manager.srvm_commands.tasks.StartTasks.py\n
            StartTasks.execute()
        
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
        
        def start_task(task: Tasks):
            """ # StartTasks command start_task method
            /!\\ This is a coroutine, it needs to be awaited
            
            Description :
            ---
                Start a specific task
                
            Access :
            ---
                src.bots.server_manager.srvm_commands.tasks.StartTasks.py\n
                StartTasks.start_task()
                
            Parameters :
            ---
                - task : :class:`Tasks` => Task to start
                
            Returns :
            ---
                :class:`None`
            """
            # Get the task class and the task list
            task_class = task.value.get("class")
            task_list = task_class.tasks_list
            task_code_name = f"{self.guild.id}-{task.value.get('name')}"

            # Set the task in the task list if not already in
            if not task_list.get(task_code_name):
                task_list.update({task_code_name: task_class(self.guild)})

            # Check if the task is a specific task
            task_code_name = f"{self.guild.id}-{self.task_name}" if self.task_name else task_code_name

            # Check if the task is running
            if task_list.get(task_code_name) and not task_list.get(task_code_name).execute.is_running():
                threading.Thread(target=task_list.get(task_code_name).start())
        
        # Start all the tasks
        for task in Tasks:
            start_task(task)

        # Send the response
        return await interaction.send(f"{task.value.get('name')} Task started") if self.task_name else await interaction.send("All tasks started")


            


            

