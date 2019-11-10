# Py_ThingSpeakRead
Python Class for reading data from ThingSpeak Platform. 

Read data from multiple Thingspeak channels and export them to csv or create Pandas dataframe for further analysis.

By default each ThingSpeak GET request may give a maximum of 8000 results. This script allows one to download all the data from a  given date range. This is achieved by sending subsequent requests until all data from that range is acquired.

For example, suppose you want to download last week's data but there are a total of 10,000 data points within that period. With a single request you can download at max 8000 data points, therefore you can't download the data for the entire week with a single request. This script will allow you define a start date and end date, and then download all the data within that period.

