from enum import Enum

class IntervalUnits(Enum):
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"

    @staticmethod
    def get_all() -> list[str]:
        """ # Get the list of intervalUnits
        ---
            Get the list of intervalUnits
        
        Access :
        ---
            src.utils.enums.intervalUnits.py\n
            intervalUnits.get_list()
        
        Returns :
        ---
            :class:`list[str]` => List of interval Unit
        """
        return [interval_unit.value for interval_unit in IntervalUnits]