import pickle, cv2, os, praw, requests
from utils.scripts.create_creds import create_token
from utils.scripts.logger import logger
import numpy as np

def RIM(sub):
    # Create directory if it doesn't exist to save images
    def create_folder(image_path):
        CHECK_FOLDER = os.path.isdir(image_path)
        # If folder doesn't exist, then create it.
        if not CHECK_FOLDER:
            os.makedirs(image_path)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(dir_path, "../../images")
    ignore_path = os.path.join(dir_path, "../ignore_images/")
    create_folder(image_path)
    try:
        os.remove(f"{image_path}/uploadme.jpg")
    except:
        pass
    # Get token file to log into reddit.
    # You must enter your....
    # client_id - client secret - user_agent - username password
    if os.path.exists('utils/creds/token.pickle'):
        with open('utils/creds/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    else:
        logger("Reddit Token Not Found. Please Create One")
        creds = create_token()
        pickle_out = open("utils/creds/token.pickle","wb")
        pickle.dump(creds, pickle_out)

    reddit = praw.Reddit(client_id=creds['client_id'],
                        client_secret=creds['client_secret'],
                        user_agent=creds['user_agent'],
                        username=creds['username'],
                        password=creds['password'])

    global img_notfound
    img_notfound = cv2.imread(ignore_path+'/imageNF.png')
    subreddit = reddit.subreddit(sub)
    logger("**************************************************************************************", "white")
    logger(f"Yoinking An r/{sub} Image!", "cyan")
    for submission in subreddit.new(limit=1):
        try:
            titleF = open("./utils/scripts/title.txt", "w")
            titleF.write(submission.title)
            titleF.close()
        except:
            titleF = open("./utils/scripts/title.txt", "w")
            titleF.write("Follow for more!")
            titleF.close()

        if "jpg" in submission.url or "png" in submission.url:
            try:
                resp = requests.get(submission.url, stream=True).raw
                image = np.asarray(bytearray(resp.read()), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)

                # Could do transforms on images like resize!
                compare_image = cv2.resize(image,(224,224))

                # Get all images to ignore
                for (dirpath, dirnames, filenames) in os.walk(ignore_path):
                    ignore_paths = [os.path.join(dirpath, file) for file in filenames]
                ignore_flag = False

                for ignore in ignore_paths:
                    ignore = cv2.imread(ignore)
                    difference = cv2.subtract(ignore, compare_image)
                    b, g, r = cv2.split(difference)
                    total_difference = cv2.countNonZero(b) + cv2.countNonZero(g) + cv2.countNonZero(r)
                    if total_difference == 0:
                        ignore_flag = True

                if not ignore_flag:
                    if(image.shape[0] >= (image.shape[1]*0.5) or image.shape[1] >= (image.shape[0]*0.5)):
                        scale_percent = 90 # percent of original size
                        width = int(image.shape[1] * scale_percent / 100) #Yuck
                        height = int(image.shape[0] * scale_percent / 100) #Math
                        dim = (width, height)
                        src = cv2.resize(image, dim, interpolation = cv2.INTER_AREA) #Resized the fucker
                        cv2.imwrite(f"{image_path}/uploadme.jpg", src)
                    else:
                        cv2.imwrite(f"{image_path}/uploadme.jpg", image)
            except Exception as e:
                logger(f"Couldnt grab image. {submission.url.lower()}", "cyan")
                logger(e, "red")
        else:
            logger("Unable to yoink...", "cyan")