from utils.scripts import getImage, postImage, waiter, logger
import os, json, random, time

#*************Settings*************#
with open("settings.json", "r") as read_file:
    settings = json.load(read_file) #Gets settings
repeating = settings["repeat"] #Repeat Script

minPostDelay = settings["minPostDelay"] #Min Repost Delay
maxPostDelay = settings["maxPostDelay"] #Max Repost Delay
retryDelay = settings["retryDelay"] #Retry Delay

mDesc = settings["mDesc"] #Any more info to each posts description 
allowLogs = settings["allowLogs"] #Send logs to the console

switch = 0 #Switch between each sub
subs = settings["subs"] #Each sub
tags = settings["tags"] #Each tag
#*************Settings*************#

def tasks():

    global switch
    postDelay = random.randrange(minPostDelay, maxPostDelay, 5)
    #************************#
    if(switch >= len(subs)):
        switch=0
    getImage.RIM(subs[switch])
    #************************#
    try:
        if os.path.exists("./images/uploadme.jpg"):
            postImage.resizeImages()
            returnVal = postImage.postFinal(subs[switch], tags, mDesc)
            switch+=1
            if(returnVal == 0): waiter.waitInput(0, postDelay, repeating, switch)
            if(returnVal == 1): waiter.waitInput(1, retryDelay, repeating, switch)
        else:
            waiter.waitInput(1, retryDelay, repeating, switch)
        tasks()
    except Exception as e:
        logger.logger(e, "red")

if not os.path.exists("./utils/creds"):
    os.mkdir("./utils/creds")
print("Anime Instagram bot - V2.1.1 CREATED BY IGNOREDSOUL")
postImage.createLogin()
postImage.login()
tasks()
