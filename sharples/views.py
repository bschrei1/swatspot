from django.shortcuts import render
from django.http import HttpResponse
from sharples.models import Update, Interval
from django.template import RequestContext, loader
from django.utils import timezone
import datetime

def index(request):
    
    
    currTime= datetime.datetime.now()
    latestUpdateList= Update.objects.order_by('-when')
    secondLatestUpdate=latestUpdateList[0]
    newUpdate = Update(when=currTime)
    newUpdate.save()

    latest_interval_list = Interval.objects.order_by('-startTime')

    latest_update_list = Update.objects.order_by('-when')[:15] 
    # chose 5, but I was not sure how many updates I entered into the DB
    #need to call computeInterval here
    template = loader.get_template('sharples/index.html')
    context = RequestContext(request,{'latest_update_list': latest_update_list,})
    return HttpResponse(template.render(context))
"""    
    percentile = computeInterval(15)
    # chose 5, but I was not sure how many updates I entered into the DB
    template = loader.get_template('sharples/index.html')
    context = RequestContext(request,{'percentile': percentile})
    return HttpResponse(template.render(context))

def computeInterval(paramSeconds):
    #compute an interval containing the number of swipes between the time
    #of request and paramSeconds, a parameterized amount of time.
    currTime = datetime.datetime.now()
    sorted_update_list = Update.objects.order_by('-when')
    #currTime = sorted_update_list[0]
    countedUpdates = 1  # the number of updates in a time interval
    intEndTime = currTime #default endTime of the interval
    
    for update in sorted_update_list:
        #if update occured less than paramSeconds before currUpdate
        if (currTime - update.when).seconds < paramSeconds :
            countedUpdates += 1
            if countedUpdates == 2:
                intEndTime = update.when
        else if countedUpdates > 1: #if there are updates besides currUpdate
            currInterval = Interval(endTime = intEndTime, startTime = currTime, numUpdates = countedUpdates)
            currInterval.save()
            break
        """
    
def students(request):
    print "called"
    #latest_update_list = Update.objects.all()
    updates = Update.objects.order_by('-when')
    latest_update = updates[0]#Update.objects.get(id=len(latest_update_list))
    print latest_update
    
    template = loader.get_template('students/indexStudents.html')
    latest_update_list = Update.objects.order_by('-when')
    percentileOfLatestInterval = computePercentile(latest_update_list, 500)
    context = RequestContext(request,{'latest_update': latest_update, 'percentile':percentileOfLatestInterval, 'interval': Interval(endTime=datetime.datetime.now(), startTime=datetime.datetime.now(), numUpdates=6)})

    return HttpResponse(template.render(context))

def computePercentile (sorted_update_list, paramSeconds):
    countedUpdates = 1
    #countedUpdates = 0 #TODO comment out this line
    sortedIntervals = Interval.objects.order_by('-numUpdates') #descending order: newest at pos 0  
    print "len sorted intervals line 70", len(sortedIntervals)
    #currTime = datetime.datetime.now() #TODO: uncomment this line
    currTime = datetime.datetime(2014, 11, 25, 06, 25, 53) #TODO: delete this line (was for testing purposes)
    #currTime = sorted_update_list[0].when.replace(tzinfo=None) #get the most current update in the db
    print currTime, "line 75 currTime"
    intEndTime = currTime #default endTime

    print sorted_update_list
    for update in sorted_update_list:
        updateCpy = update
        naive = updateCpy.when.replace(tzinfo=None)
        #print naive
        #print (currTime - naive).seconds, "line 83 currTime -update.when", (currTime - naive).days,
        
        #if update occured less than paramSeconds before currUpdate
        if (currTime - naive).seconds < paramSeconds and (currTime - naive).days >= 0:
            print (currTime - naive).seconds, "line 83 currTime -update.when"
            countedUpdates += 1 #add to the number of swipes that happened in that interval
            if countedUpdates >= 2:
                intEndTime = update.when
        elif countedUpdates >=1: #if we have finished checking this interval
            currInterval = Interval(endTime = intEndTime, startTime = currTime, numUpdates = countedUpdates-2)
            break #leave for loop once we are done checking

        
    position = 0 #compare the interval with the most updates first
        
    for interval in sortedIntervals: #compute swipes percentile of currInterval
        #print "in for loop line 90"
        #print currInterval.numUpdates, "numUpdates line 91"
        #print interval.numUpdates, "interval numUpdates line 92"
        if currInterval.numUpdates < interval.numUpdates:
            print currInterval.numUpdates, interval.numUpdates, "line 103"
            position +=1

        else:
            break
    print position

    percentile = float(len(sortedIntervals)-position)/len(sortedIntervals)
    #percentile = percentile -.01
    print percentile
    return percentile

def detail(request, update_id):
    return HttpResponse("You're looking at update %s." % update_id)


# Create your views here.
