# ThingSpeak Python Client

Access the data on ThingSpeak platform through its Read API.

### ThingSpeakRead.py
Download data from ThingSpeak as Pandas dataframe or export as CSV.

By default, each ThingSpeak read request will return a maximum of 8000 data points. Therefore, several requests may be necessary to download the complete dataset from a given period. This script allows one to download the complete dataset from an arbitrary time period by automatically sending subsequent requests.
