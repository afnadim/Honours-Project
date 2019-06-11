import time
import datetime

print(datetime.datetime.now())



localtime = time.asctime(time.localtime(time.time()))
print ("Local current time :", localtime)
