__author__ = 'estsauver'
import datetime
import sqlalchemy
from twilio.rest import TwilioRestClient

#My twilio account credentials. Please don't steal them. Kim.
account = "AC8c55c6e9f0c1dd3532c3302b36ff5179"
token = "c8908533bb3ed7698cfac71832747657"
client = TwilioRestClient(account, token)

class ErrorHandler(object):
    def __init__(self, experiment):
        #newerrorhandler = ErrorHandler(experimentWeHave)
        self.experiment = experiment
        #Sets maximum time between alerts so we're not constantly getting phone calls. This is right now 30 mins.


    #Actual sends the text message out.
    def alert(self, bodyText="There's a problem with the reactor"):
        '''Sends an alert if one has not been sent in the last 30 minutes.
        '''
        #Last Alert
        self.experiment.session.query("alerts").first()

        #If loop makes sure we haven't sent one recently.
        if len(self.alertHistory) > 0:
            if (self.alertHistory[-1][2] - datetime.datetime.now()) > datetime.timedelta(seconds=self.alertInterval):
                self.sendMessage(bodyText)
        else:
            self.sendMessage(bodyText)
            print "Would have sent message"

    def sendMessage(bodyText):
        message = client.sms.messages.create(to="+18572378675", body=bodyText, from_="+17694473275")
        self.alertHistory.append((message, datetime.datetime.now()))
        print message


    def newError(self, type, values, time = datetime.datetime.now()):
        self.badData.flush()
        self.BadData.add_bad_data(self.badData, type, time, values)
        self.checkAlertConditions()


    def checkAlertConditions(self):
        #This calls all of the functions which separately determine the existence of a problem. Each of the functions
        # can separetly process control scheme logic.
        self.badDataCount()

    def badDataCount(self):
        if self.badData.count() > 5:
            self.alert(bodyText="5 recent bad data messages")
            return True

    class BadData(object):
        def __init__(self):
            self.data = []
            #The amount of time that we remember bad data for
            self.badDataMemory = 1000

        #get rid of old bad data. Called when we get new bad data!

        def flush(self):
            if len(self.data)>0:
                while (datetime.datetime.now() - self.data[0][1]) > datetime.timedelta(seconds=self.badDataMemory):
                    self.data.pop()

        def add_bad_data(self, type, time, values):
            self.data.append((type, time, values))

        def count(self):
            return len(self.data)



