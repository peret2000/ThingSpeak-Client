# Py_ThingSpeakRead
Python Class for reading data from ThingSpeak Platform. 

Read data from multiple Thingspeak channels and export them to csv or create Pandas dataframe for further analysis.

By default each ThingSpeak GET request may give a maximum of 8000 results. This script allows one to download all the data from a  given date range by sending subsequent requests until all data from that range is acquired.
