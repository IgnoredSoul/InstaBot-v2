import json
from termcolor import colored

with open("settings.json", "r") as read_file:
    settings = json.load(read_file) #Gets settings
allowLogs = settings["allowLogs"]

def logger(log, color):
    if(allowLogs == True):
        print("> " + colored(f"{log}", color))
    else:
        pass
