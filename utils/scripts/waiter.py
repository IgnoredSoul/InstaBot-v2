import time, pytz, datetime
from utils.scripts.logger import logger
count = 1
fmt = '%Y/%m/%d %H:%M'


def waitInput(yn, delay, repeating, switch):
    if(repeating == True):

        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        pst_now = utc_now.astimezone(pytz.timezone("Australia/South"))
        pst_now = pst_now.strftime(fmt)
        _delayTime = str(delay/3600)
        delayTime = _delayTime[:3]
        global count

        if(yn == 0):
            logger("**************************************************************************************", "white")
            logger(f"  Task count: {count} | Switch count: {switch} | {pst_now} | Next post is in: {delayTime} hours", "green")
            time.sleep(delay)
            count+=1
        if(yn == 1):
            time.sleep(delay)