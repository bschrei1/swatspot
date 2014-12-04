from django.db import models
import datetime

# Create your models here.
class Update(models.Model):
   #pubDate = models.DateField('date published')
   #weekDay = models.CharField(max_length = 200) #eg Friday or Saturday
   #timeOfDay = models.TimeField() #haven't decided whether it will be military
   #swipes = models.AutoField()
   when = models.DateTimeField('time of swipe')
   eventType = models.CharField(max_length=200)

   def __str__(self):
       day = self.when.strftime('%A')
       time = self.when.strftime('%H:%M:%S')
       return '%s on %s at %s' % (self.eventType, day, time)

   def getDay(self):
       return self.when.strftime('%A')



class Interval(models.Model):
    endTime = models.DateTimeField('time of last swipe in the interval')
    startTime = models.DateTimeField('time of first swipe in the interval')
    numUpdates = models.IntegerField(default=0) #number of swipes that ocurred in the interval
    def __str__(self):
       day = self.endTime.strftime('%A')
       time1 = self.startTime.strftime('%H:%M:%S')
       time2 = self.endTime.strftime('%H:%M:%S')

       return 'Interval on %s beginning at %s, ending at %s has %d entries' % (day, time1, time2, self.numUpdates)

