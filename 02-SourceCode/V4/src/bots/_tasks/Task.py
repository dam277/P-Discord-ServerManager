from ..Base import Base
import nextcord
from nextcord.ext import commands, tasks

from ...utils.logger.Logger import Logger, LogDefinitions

class Task(Base):
    tasks_list: dict[int, "Task"] = {}
    """ # Task class
    
    Description :
    ---
        Manage Tasks as a parent of all of them
        
    Access :
    ---
        src.bots.server_manager.Tasks.Task.py\n
        Task
    
    inheritance :
    ---
        - Base : :class:`Base` => Parent class of all commands
    """

    def trigger(name: str):
        """ # Trigger decorator

        Description :
        ---
            Decorate a function to be a trigger

        Access :
        ---
            src.bots.server_manager.Tasks.Task.py\n
            Task.trigger()

        Parameters :
        ---
            - name : :class:`str` => Name of the Task
        
        Returns :
        ---
            :class:`function`
        """
        def decorator(func):
            """ # Trigger decorator
            
            Description :
            ---
                Decorate a function to be a trigger
                
            Access :
            ---
                src.bots.server_manager.Tasks.Task.py\n
                Task.trigger()
            
            Parameters :
            ---
                - func : :class:`function` => Function to decorate
                
            Returns :
            ---
                :class:`function`
            """
            def wrapper(self: Task, *args, **kwargs):
                """ # Trigger wrapper 

                Description :
                ---
                    Wrapper of the trigger decorator

                Access :
                ---
                    src.bots.server_manager.Tasks.Task.py\n
                    Task.trigger().wrapper()

                Parameters :
                ---
                    - self : :class:`Task` => Task object
                    - *args : :class:`list` => Positional arguments
                    - **kwargs : :class:`dict` => Keyword arguments

                Returns :
                ---
                    :class:`function`
                """
                message = f"{name} Task triggered"
                Logger.log(LogDefinitions.INFO, message)
                return func(self, *args, **kwargs)
            return wrapper
        return decorator
    
    @tasks.loop(seconds=5)
    async def execute(self, interation: nextcord.Interaction):
        """ # Task class execute method
        
        Description :
        ---
            Execute the Task

        Access : 
        ---
            src.bots.Task.py\n
            Task.execute()

        Parameters :
        ---
            interation : :class:`nextcord.Interaction`

        Returns : 
        ---
            :class:`None`
        """
        pass

    def start(self, guild_id: int):
        """ # Task start method
        
        Description :
        ---
            Start the task
            
        Access :
        ---
            src.bots.server_manager.Tasks.Task.py\n
            Task.start()
        
        Returns :
        ---
            :class:`None`
        """
        pass

    def stop(self):
        """ # Task stop method
        
        Description :
        ---
            Stop the task
            
        Access :
        ---
            src.bots.server_manager.Tasks.Task.py\n
            Task.stop()
        
        Returns :
        ---
            :class:`None`
        """
        pass