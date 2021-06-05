#!/usr/bin/env python3
# Author: Jabir Bin Jahangir (github.com/kanjiowl)

import requests, json
import urllib.parse 
from zipfile import ZipFile
import pandas as pd
import datetime

# Thingspeak client class 
class ThingSpeakClient:
    '''
    ThingSpeak Client class 
    '''


    def __init__(self, channelID, readKey, tz="US/Central"):  
        '''
        ThingSpeakClient class init
            
        Arguments: 
            channelID {list}  -- List of channel ids 
            readKey {list} -- List of ThingSpeak read API keys
            tz {string}  -- Time zone

        '''

        # init vars
        self.base_r = "https://api.thingspeak.com/channels/{0}/feeds.json?&api_key={1}"
        self.api_r = []
        self.n_r= 0 # Number of channels to read from  
        self.date_suffix = "%2000:00:00"
        self.data_feeds = [] 
        self.tz = ''


        self.channelID = channelID
        self.readKey = readKey
        self.tz = tz

        if len(self.channelID) ==  len(self.readKey): 
            self.n_r = len(self.channelID)
            self.data_feeds = [[] * self.n_r for i in range(self.n_r)]
            for ind in range(0, len(self.channelID)):
                self.api_r.append(self.base_r.format(self.channelID[ind], self.readKey[ind]))


    def read(self,res):
        '''
            Deprecated read function 
        '''
        for ind in range(0, self.n_r):  
            r = self.api_r[ind] + "&results={0}".format(res)
            print(r)
            req = requests.get(r).json()
            # print(json.dumps(req.json(), indent=2));
            self.data_feeds[ind] = pd.DataFrame(req["feeds"])
            # convert field data to floats
            self.data_feeds[ind].iloc[:, range(2,10)] = self.data_feeds[ind].iloc[:, range(2,10)].apply(pd.to_numeric) 
            self.data_feeds[ind][["created_at"]] = self.data_feeds[ind][["created_at"]].apply(pd.to_datetime)
            self.data_feeds[ind]["created_at"]= self.data_feeds[ind]["created_at"].dt.tz_convert(self.tz)  
            # self.data_feeds[ind].set_index('created_at', inplace=True, drop=True) 
        return self.data_feeds


    def readRange(self, start, end):
        """[Read data from a given date range. Allows bypassing the ThingSpeak's 8000 results limit per request.]

        Arguments:
            start {list} -- [YY, MM, DD, h, m, s]
            end {list} -- [YY, MM, DD, h, m, s]

        Returns:
            [pandas dataframe] -- [Returns a Pandas Dataframe array where each array element contains data from each channel.]
        """
        self.data_feeds = []
        self.data_feeds = [[] * self.n_r for i in range(self.n_r)]

        for ind in range(0, self.n_r):

            print("SENDING REQUEST FOR CHANNEL:: {0}".format(ind+1))

            self.start = self.time_string(start) # start + self.date_suffix ;
            self.end = self.time_string(end) #end+ self.date_suffix ;

            # Data request loop 
            while True: 
                r = self.api_r[ind] + \
                    "&start={0}&end={1}&timezone={2}" \
                    .format(self.start, self.end, urllib.parse.quote(self.tz , safe='')) 

                data = requests.get(r).json();   # Get the JSON response 

                # Debug print
                print("Feed Length::  " + str(len(data["feeds"])) )
                print(r)

                if len(data['feeds']) == 1 :
                    self.data_feeds[ind] = data["feeds"] + self.data_feeds[ind] 
                    break
                else :
                    self.data_feeds[ind] = data["feeds"][1:] + self.data_feeds[ind] 
                    d_str = data["feeds"][0]["created_at"][0:10]
                    t_str = data["feeds"][0]["created_at"][11:19]
                    self.end = d_str + "%20"+t_str

            # print(json.dumps(self.data_feeds, indent=2))

            # Create pandas dataframe
            self.data_feeds[ind] = pd.DataFrame(self.data_feeds[ind]) 
            self.data_feeds[ind].iloc[:, range(2,10)] = self.data_feeds[ind].iloc[:, range(2,10)].apply(pd.to_numeric) 
            self.data_feeds[ind][["created_at"]] = self.data_feeds[ind][["created_at"]].apply(pd.to_datetime)  

            # self.data_feeds[ind].set_index('created_at', inplace=True, drop=True)
            # self.data_feeds[ind]["created_at"]= self.data_feeds[ind]["created_at"].dt.tz_convert(self.tz)        
        return self.data_feeds;

    def readAll(self):
        pass

    ## Utility methods 
    def time_string(self,datearray):
        ''' 
            Convert tuple to datetime string
            2 types of datetime string format:
                 - for api request
                    - input : a tuple (YY, MM, DD, h, m, s, timezone)
                    - output : YYYY-MM-DD%20HH:MM:SS
                 - JSON response date format
        ''' 
        try: 
            year, month, day, hour, minute, second = datearray 
            return urllib.parse.quote(datetime.datetime(
                year, month, day, hour, minute, second).strftime("%Y-%m-%d %H:%M:%S"), safe='-:')
        except ValueError:
            raise Exception("Make sure date array contains [YY, MM, DD, h, m, s] ")

    def saveCSV(self):
        ''' 
        [Outputs the channel data in CSV format.] 
        '''
        print('Saving to csv')
        for ind in range(0, self.n_r):
            self.data_feeds[ind].to_csv(r"./data_channel{}.csv".format(ind+1), index=False)

    def saveZip(self):
        '''
        Output the CSV to zip file for distribution 
        '''
        with ZipFile('data.zip', 'w') as zip:
            for ind in range(0, self.n_r):
                filename = r"data_channel{}.csv".format(ind+1)
                self.data_feeds[ind].to_csv(filename)
                zip.write(filename)
            zip.close();


