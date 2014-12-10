from django.shortcuts import render
from django.http import HttpResponse
from sharples.models import Update, Interval
from django.template import RequestContext, loader
from django.utils import timezone
import datetime

def index(request):
    
    
    currTime= datetime.datetime.now()
    latestUpdateList= Update.objects.order_by('-when')#new to old
    secondLatestUpdate=latestUpdateList[0]
    newUpdate = Update(when=currTime, eventType = "swipe")
    newUpdate.save()

    

    latest_update_list = Update.objects.order_by('-when')[:15] 
    template = loader.get_template('sharples/index.html')
    context = RequestContext(request,{'latest_update_list': latest_update_list,})
    return HttpResponse(template.render(context))



"""This program computes the crowdedness percentile of Sharples based on the 
time of an HTTP request to our site. It looks through all the historical data and sees which swipes occured within a parametrized amount of time, paramSeconds, which is defined above. It then looks through the database and computes the amount of elapsed time such that there were fewer or as many swipes within this amount of time (i.e. computes the amount of time such that there were fewer or as many people in the building). Maybe we can extend the application beyond Sharples, but for the sake of simplicity, I write comments as if it only applies to Sharples.

Ben Schreiber 12/6/14
"""

def students(request):
    paramSeconds = 2400 #40 mintutes
    allUpdates = Update.objects.all() #Django command to retrieve all Update events in its database
    allUpdates = allUpdates.order_by('-when') #sort newest to oldest
    sharplesIsOpen = sharplesIsOpenNow(allUpdates) #see if Sharples is currently open
    if not sharplesIsOpen:   #if sharples is closed
        
        percentile =0
        percentileComplement = 1   #message, crowdedness percentile, 1 - crowdednes percentile
    else:
        allUpdates = formatTimeData(allUpdates) 
        (numCurrRecentUpdates, httpRequestTime) = computeCurrRecentUpdates(allUpdates, paramSeconds) #currRecentUpdates= list of swipes w/in paramSeconds of httpRequestTime
    
    
        elapsedTimeDict = {} #keys are number of people in Sharples, values are elapsed time in seconds such that this has been the case
        elapsedTimeDict[0] = 0 #begin with 0 minutes of 0 people
    
        newUpdate = Update(when = httpRequestTime, eventType = "httpRequest") #event signaling the time of the http request i.e when this view is called
        allUpdates.append(newUpdate)

        allUpdates = createDeathEvents(allUpdates, paramSeconds)
        elapsedTimeDict = createElapsedTimeDict(allUpdates, paramSeconds, httpRequestTime) #dict w/ number of swipes as keys, seconds elaspsed as values
        percentile = 100*computePercentile(numCurrRecentUpdates, elapsedTimeDict)
        
        percentileComplement = 1 - percentile
	
    
    context = RequestContext(request,{'sharplesIsOpen': sharplesIsOpen, 'percentile': percentile,})
    template = loader.get_template('students/indexstudents.html')
    return HttpResponse(template.render(context))


#Returns boolean whether Sharples is open (1=open, 0=closed)   
def sharplesIsOpenNow(allUpdates):
    if allUpdates[0].eventType == "closing": #if the most recent event was a closing
        return False
    
    return True #otherwise Sharples is open




#returns the number of updates that occured within paramSeconds of the time of the HTTP request
def computeCurrRecentUpdates(allUpdates, paramSeconds):
    numCurrRecentUpdates = 0 #number of updates that occured within paramSeconds of currTime
    currTime = datetime.datetime.now()
    for update in allUpdates:
        naive = update.when.replace(tzinfo = None) #django datetime objects are UTC by default
        timeDiff = (currTime-naive).total_seconds()
        if timeDiff <= paramSeconds:
            numCurrRecentUpdates+=1
            
            #TODO: add break statement here
    return (numCurrRecentUpdates, currTime)




#subtracts 5 hours off of each event in allUpdates to convert to EST from UTC. Returns new list of updates
def formatTimeData(allUpdates):
    allUpdatesCopy = [] #will insertUpdates of EST times in this list
    for update in allUpdates: 
        newUpdate = Update(when = update.when-datetime.timedelta(hours =5), eventType = update.eventType)
        allUpdatesCopy.append(newUpdate)
    #print allUpdatesCopy, "/nline 93!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    return allUpdatesCopy
        





#creates swipeDeath updates which tell us when a person has left the building. Returns list allUpdates with swipeDeaths included
def createDeathEvents(allUpdates, paramSeconds):
    deathsList = [] #list that will store swipe deaths as we loop through allUpdates
    for update in allUpdates:
        if update.eventType != "swipe": #only create death events after swipes
            continue
        if update.when.isoweekday()==7 or update.when.isoweekday() == 6: #if Sunday or Saturday, Sharples closes at 8 pm
            #print "here"
            closingTime = datetime.datetime(update.when.year, update.when.month, update.when.day, 18, 30, 00) #entries are in miliary time
        else: #week day closes at 8:00
            closingTime = datetime.datetime(update.when.year, update.when.month, update.when.day, 20, 00, 00)
        naive = update.when.replace(tzinfo = None) 
        timeTillClosing = (closingTime-naive).total_seconds() #number of seconds between update and the closing time
        
        if timeTillClosing > paramSeconds: #if not paramSeconds from closingTime create a death event
            deathTime = naive + datetime.timedelta(seconds = paramSeconds) # time of death is paramSeconds after swipe occured
            newDeath = Update(when = deathTime, eventType = "swipeDeath") 
            deathsList.append(newDeath)#changed
    
    for swipeDeath in deathsList:
        allUpdates.append(swipeDeath)
    newUpdatesList = [] #TODO delete the following lines if they don't work  
    for update in allUpdates:
        naive = update.when.replace(tzinfo = None) 
        newUpdate = Update(when = naive, eventType = update.eventType)
        newUpdatesList.append(newUpdate)
    ####################################end new
    newUpdatesList.sort(key=lambda x: x.when, reverse=False)#sort by oldest (position 0) to newest (position len(list)-1)
    allUpdates = newUpdatesList
    
    return allUpdates




#loops through allUpdates and computes the amount of time we have seen certain numbers of people in the building. 
#Returns the elapsedTimeDict storing this information: keys are number of people, values are time elapsed in seconds (believe that they're floats)
def createElapsedTimeDict(allUpdates, paramSeconds, httpRequestTime):
    elapsedTimeDict = {}
    for update in allUpdates:
        if update.eventType == "opening":
            iterativeLivingUpdates = 0 #the number of students in sharples at this time in history
            timeOfPreviousUpdate = update.when
        else: #swipe swipeDeath or closing
            timeSincePreviousUpdate = (update.when-timeOfPreviousUpdate).total_seconds()
            if iterativeLivingUpdates in elapsedTimeDict.keys(): #if we've seen this number of people in Sharples before
                elapsedTimeDict[iterativeLivingUpdates] = timeSincePreviousUpdate + elapsedTimeDict[iterativeLivingUpdates]
            else: #we have not seen this number of people in Sharples before
                elapsedTimeDict[iterativeLivingUpdates] = timeSincePreviousUpdate
            if update.eventType == "swipe":
                iterativeLivingUpdates += 1 #add 1 to iterativeLivingUpdates for swipe
            elif update.eventType == "swipeDeath":
                iterativeLivingUpdates -= 1
            #for closing or httpRequest events we don't add to iterativeLivingUpdates
            timeOfPreviousUpdates = update.when
    return elapsedTimeDict




                
#computes the amount of time elapsed s.t. there were fewer or just as many people in Sharples as there are now
def computePercentile(numCurrRecentUpdates, elapsedTimeDict):
    allKeys = elapsedTimeDict.keys()
    #numCurrRecentUpdates = len(currRecentUpdates) #estimated number of people in Sharples now
    timeEquallyOrLessCrowded = 0 #will compute this value in for loop (will be in seconds)
    totalTimeElapsed = 0 # will compute this value in for loop, as well (also in seconds)
    
    for key in allKeys:
        if key <= numCurrRecentUpdates:
            timeEquallyOrLessCrowded += elapsedTimeDict[key]
        totalTimeElapsed += elapsedTimeDict[key]
    #print timeEquallyOrLessCrowded
    #print totalTimeElapsed
    crowdednessPercentile =timeEquallyOrLessCrowded/totalTimeElapsed
    
    return crowdednessPercentile

def detail(request, update_id):
    return HttpResponse("You're looking at update %s." % update_id)

#enters an update of eventType opening when a cer
def opening(request):
    openUpdate = Update(when=datetime.datetime.now(),eventType = "opening")
    openUpdate.save()

    latest_update_list = Update.objects.order_by('-when')[:15] 
    template = loader.get_template('sharples/index.html')
    context = RequestContext(request,{'latest_update_list': latest_update_list,})
    return HttpResponse(template.render(context))


def closing(request):
    closeUpdate = Update(when=datetime.datetime.now(),eventType = "closing")
    closeUpdate.save()
    latest_update_list = Update.objects.order_by('-when')[:15] 
    template = loader.get_template('sharples/index.html')
    context = RequestContext(request,{'latest_update_list': latest_update_list,})
    return HttpResponse(template.render(context))





