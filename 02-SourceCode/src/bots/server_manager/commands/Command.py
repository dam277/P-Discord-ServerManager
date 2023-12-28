import json

class Command:
    """ Command parent class """
    def __init__(self):
        """ Get the settings of the discord bot """
        s = open("src/resources/configs/settings.json")
        self.settings = json.load(s)