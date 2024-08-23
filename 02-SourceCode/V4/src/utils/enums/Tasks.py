from enum import Enum

from ...bots._tasks.Task import Task

from ...bots.server_manager.srvm_tasks import CheckDistantServerActivity

class Tasks(Enum):
    check_distant_server_activity: dict[str, Task] = {"name": "distant server activity", "class" : CheckDistantServerActivity}

    @staticmethod
    def get_all() -> list[str]:
        """ # Get the list of tasks
        ---
            Get the list of tasks
        
        Access :
        ---
            src.utils.enums.Tasks.py\n
            Tasks.get_list()
        
        Returns :
        ---
            :class:`list[str]` => List of tasks
        """
        return [task.value["name"] for task in Tasks]