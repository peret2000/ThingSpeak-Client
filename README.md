# ThingSpeak Read API Python Client

Access the data on ThingSpeak platform through its Read API.

# ThingSpeakRead.py
Access data from defined Thingspeak channels and export them to CSV file or create Pandas dataframe for further analysis.

By default, each ThingSpeak read request will return a maximum of 8000 data points. Therefore, several requests are necessary to download the complete dataset from a given period. This script allows one to download all the data from arbitrary time period by automatically sending subsequent requests.
