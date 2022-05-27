from utils.scripts.logger import logger
from utils.scripts.create_creds import create_login
from utils.scripts.waiter import waitInput
from datetime import datetime
from instagrapi import Client as Bot
import pickle, os, cv2

def createLogin():
    if not os.path.exists('./utils/creds/login.pickle'):
        logger("\nInstagram Login Not Found. Please Create One")
        creds = create_login() #Custom function that makes the info
        pickle_out = open("./utils/creds/login.pickle","wb")
        pickle.dump(creds, pickle_out) #Saves the login and uses it the next time

def login():
    try:
        global bot
        with open('./utils/creds/login.pickle', 'rb') as token:
            lgin = pickle.load(token) #Gets login info
        bot = Bot() #Yeah
        bot.login(lgin['username'], lgin['password']) #Logs in with the .pickle file
    except Exception as e:
        logger(e, "red") #If theres ever an error :|

def resizeImages():
    src = cv2.imread('./images/uploadme.jpg', cv2.IMREAD_UNCHANGED)
    while(src.shape[0] > 1080 and src.shape[1] > 1080):
        scale_percent = 90 # percent of original size
        width = int(src.shape[1] * scale_percent / 100) #Yuck
        height = int(src.shape[0] * scale_percent / 100) #Math
        dim = (width, height)
        src = cv2.resize(src, dim, interpolation = cv2.INTER_AREA) #Resized the fucker
        cv2.imwrite("./images/uploadme.jpg", src)
        
    global title
    titleF = open("./utils/scripts/title.txt", "r")
    title = titleF.read() #Makes "title" a global string
    titleF.close()

def postFinal(sub, tags, mDesc):
    specialChars = "[]\'"
    for specialChar in specialChars:
        tags = str(tags).replace(specialChar, ' ')
    try:
        _finalCaptions = f"r/{sub} - {title}\n↡Tags↡\n{tags}\n\n{mDesc}" #Puts the caption together
        logger(f"Uploading Image", "cyan")
        bot.photo_upload("./images/uploadme.jpg", _finalCaptions) #Upload
        logger(f"Uploaded Success", "green")
        return(0)
    except Exception as e:
        logger("Upload Failed", "cyan")
        logger(e, "red") #If theres ever an error :|
        return(1)
