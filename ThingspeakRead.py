#!/usr/bin/python3
# Author: Jabir Bin Jahangir

import requests, json
import pandas as pd

# Thingspeak API class on Python3
# Outputs the data as Pandas dataframe
# Allows reading from multiple channels.
# Allows reading for any given - will allow reading more than 8000 data point.

class ThingspeakRead:
    base_r = "https://api.thingspeak.com/channels/{0}/feeds.json?api_key={1}";
    api_r = [];
    n_r= 0
    date_suffix = "%2000:00:00"
    data_feeds = [[], []]
    tz = ''
    def __init__(self, channelID, readKey, tz="US/Central"):  
        self.channelID = channelID; 
        self.readKey = readKey;
        self.tz = tz
        if len(self.channelID) ==  len(self.readKey): 
            self.n_r = len(self.channelID)
            for ind in range(0, len(self.channelID)):
                self.api_r.append(self.base_r.format(self.channelID[ind], self.readKey[ind]))

    def read(self,res):
        for ind in range(0, self.n_r):  
            r = self.api_r[ind] + "&results={0}".format(res)
            req = requests.get(r).json();
            # print(json.dumps(req.json(), indent=2));
            self.data_feeds[ind] = pd.DataFrame(req["feeds"]);
            # convert field data to floats
            self.data_feeds[ind].iloc[:, range(2,10)] = self.data_feeds[ind].iloc[:, range(2,10)].apply(pd.to_numeric) 
            self.data_feeds[ind][["created_at"]] = self.data_feeds[ind][["created_at"]].apply(pd.to_datetime)
            self.data_feeds[ind]["created_at"]= self.data_feeds[ind]["created_at"].dt.tz_convert(self.tz)   

        return self.data_feeds;

    def readRange(self, start, end):
        """[Read data from a given range. Allows bypassing the 8000 results limit per request.]
        
        Arguments:
            start {[string]} -- [Format: YYYY-MM-DD]
            end {[string]} -- [Format: YYYY-MM-DD]
        
        Returns:
            [pandas dataframe] -- [description]
        """

        for ind in range(0, self.n_r):
            print("SENDING REQ FOR CHANNEL :: {0}".format(ind+1));
            self.start = start + self.date_suffix ;
            self.end = end+ self.date_suffix ;
            # send request until feed becomes zero
                ## send  a request
                ## check if feed is zero
                ## if not zero set startdate with given startdate and set end date with first field date and repeat

            while True: 
                r = self.api_r[ind] + "&start={0}&end={1}".format(self.start, self.end)
                print(r)
                data = requests.get(r).json();
                print("feedlen == " + str(len(data["feeds"])) )
                self.data_feeds[ind] = data["feeds"] + self.data_feeds[ind];
                if len(data['feeds']) == 0 :
                    break
                else : 
                    d_str = data["feeds"][0]["created_at"][0:10];
                    # would miss data within 1s
                    t_str = data["feeds"][0]["created_at"][11:18] + str(int(data["feeds"][0]["created_at"][18]) - 1);
                    self.end = d_str + "%20"+t_str;  

        # print(json.dumps(self.data_feeds, indent=2))
            self.data_feeds[ind] = pd.DataFrame(self.data_feeds[ind]);
            self.data_feeds[ind].iloc[:, range(2,10)] = self.data_feeds[ind].iloc[:, range(2,10)].apply(pd.to_numeric) 
            self.data_feeds[ind][["created_at"]] = self.data_feeds[ind][["created_at"]].apply(pd.to_datetime)  
            self.data_feeds[ind]["created_at"]= self.data_feeds[ind]["created_at"].dt.tz_convert(self.tz)        
        return self.data_feeds;

    def readAll(self):
        return

    def toCSV(self):
        for ind in range(0, self.n_r):
            self.data_feeds[ind].to_csv(r".\data_channel{}.csv".format(ind+1))