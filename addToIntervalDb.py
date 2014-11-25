import random 
import datetime
import time
from sharples.models import Interval, Update
#import fake updates into updates db and fake update intervals into interval db for purpose of testing
def main():
    timeA = datetime.datetime.now()
    
    for i in range (1, 10):
        time.sleep(random.uniform(0.0,0.5))
        timeB = datetime.datetime.now()
        randNum = random.randint(2,10)
        interval = Interval(endTime = timeB, startTime = timeA, numUpdates = randNum)
        update = Update(when = timeA)
        update.save()
        interval.save()
        timeA=timeB
    
    update = Update(when = timeB)
    update.save()   














main()
