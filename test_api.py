#!/usr/bin/python3

# Routines for testing the ThingSpeakClient

from ThingSpeakClient import ThingSpeakClient
import os.path 

# Test definitions
def test_readRange(): 
    client = ThingSpeakClient([819840],["064FW8NTX3QRY4QP"], tz='Asia/Dhaka')
    dat = client.readRange([2019,11,13,0,0,0 ], [2019,11,14,0,0,0] )
    print(dat[0].head()) 
    print(dat[0].tail())
    assert len(dat[0]) == 718

def test_saveCSV(): 
    client = ThingSpeakClient([819840],["064FW8NTX3QRY4QP"], tz='Asia/Dhaka')
    dat = client.readRange([2019,11,13,0,0,0 ], [2019,11,14,0,0,0] )
    client.saveCSV()
    assert os.path.isfile('./data_channel1.csv')


# Run tests 
test_readRange(); 
test_saveCSV(); 
