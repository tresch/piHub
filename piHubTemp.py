#!/usr/bin/python
# raspberry pi nrf24l01 hub
# more details at http://blog.riyas.org
# Credits to python port of nrf24l01, Joao Paulo Barrac & maniacbugs original c library

import sys
sys.path.insert(0, '../nrf24pihub')
import nrf24

from nrf24 import NRF24

import time
from time import gmtime, strftime

import MySQLdb

# sleep at startup to let the db come up
time.sleep(15)

pipes = [[0xf0, 0xf0, 0xf0, 0xf0, 0xe1], [0xf0, 0xf0, 0xf0, 0xf0, 0xd2]]

radio = NRF24()
radio.begin(0, 0,25,18) #set gpio 25 as CE pin
radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(0x4c)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(1)
radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])

radio.startListening()
radio.stopListening()

radio.printDetails()
radio.startListening()

airTemp = "0"
poolTemp = "0"
garageFeet = "0"
garageInches = "0"
garageTemp = "0"
ble1Feet = "0"
ble2Feet = "0"
ble3Feet = "0"
tvRoomTemp = "0"

lastGarageTime = ""
lastPoolTime = ""
lastBle1Time = ""
lastBle2Time = ""
lastBle3Time = ""
lastTvRoomTime = ""
lastPoolPayload = ""
lastGaragePayload = ""
lastBle1Payload = ""
lastBle2Payload = ""
lastBle3Payload = ""
lastTvRoomPayload = ""


while True:
    pipe = [0]
    while not radio.available(pipe, True):
        time.sleep(1000/1000000.0)
    recv_buffer = []
    radio.read(recv_buffer)
    out = ''.join(chr(i) for i in recv_buffer)
    print out

    # if node is POOL, data[0] will be air temp, data[1] will be the pool. Need a third.
    dataPoints = out.split(",");

    f = open('/media/disk1/www/html/temp.html', 'w')
    f.write('<html><body style="background-color:lightblue;">')

    # if node is POOL, data[0] will be air temp, data[1] will be the pool. Need a third. 
    if(dataPoints[0] == 'POOL'):
        airTemp = dataPoints[3];
        poolTemp = dataPoints[2];

        # pool data
        f.write('<div style="font-size:60px;background-color:blue;color:white;padding:10px;border:3px solid black">Pool: ' +poolTemp + '&deg;F - Box: ' + airTemp + '&deg;F</div>')
        f.write('<br><br>')

        # tvroom data
        f.write('<div style="font-size:60px;background-color:blue;color:white;padding:10px;border:3px solid black">TV Room: ' + tvRoomTemp + '&deg;F</div>')
        f.write('<br><br>')

        # Door and car data
        intGarageFeet = int(float(garageFeet))
        if(intGarageFeet < 2):
            f.write('<div style="font-size:60px;background-color:darkred;color:white;padding:10px;border:3px solid black">Garage Door is Open.</div>')
        elif(intGarageFeet >= 2 and intGarageFeet < 6):
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Garage Door is Closed. Not Empty.</div>')
        else:
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Garage Door is Closed. Empty.</div>')

        f.write('<br><br>')

        # Temp and distance output
        f.write('<div style="background-color:gray;color:white;padding:10px;border:3px solid black">')
        f.write('<div style="font-size:60px">Garage: ' + garageTemp + '&deg;F.</div>')
        f.write('<div style="font-size:40px">Garage: ' + garageFeet + ' ft. / ' + garageInches + ' in.</div>')
        #f.write('<div style="font-size:40px">Garage: ' + garageInches + ' in.</div>')
        f.write('</div>')
        f.write('<br><br>')

        # Ble1 data and Ble2 and Ble3 data
        intBle1Feet = int(float(ble1Feet))
        intBle2Feet = int(float(ble2Feet))
        intBle3Feet = int(float(ble3Feet))
        if(intBle1Feet > 0 and intBle1Feet <= 18):
            f.write('<div style="font-size:60px;background-color:darkred;color:white;padding:10px;border:3px solid black">Dotty is on Julia&#39;s bed!</div>')
        elif(intBle2Feet > 0 and intBle2Feet < 18):
            f.write('<div style="font-size:60px;background-color:darkblue;color:white;padding:10px;border:3px solid black">Dotty is on her bed!</div>')
        elif(intBle3Feet > 0 and intBle3Feet < 30):
            f.write('<div style="font-size:60px;background-color:darkblue;color:white;padding:10px;border:3px solid black">Dotty is in the living room!</div>')    
        else:
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Dotty is not on a bed.</div>')

        f.write('<br><br>')

        lastPoolPayload = out
        lastPoolTime = time.strftime("%c")

    elif(dataPoints[0] == 'TVROOM'):
        tvRoomTemp = dataPoints[2]

        # pool data
        f.write('<div style="font-size:60px;background-color:blue;color:white;padding:10px;border:3px solid black">Pool: ' +poolTemp + '&deg;F - Box: ' + airTemp + '&deg;F</div>')
        f.write('<br><br>')

        # tvroom data
        f.write('<div style="font-size:60px;background-color:blue;color:white;padding:10px;border:3px solid black">TV Room: ' + tvRoomTemp + '&deg;F</div>')
        f.write('<br><br>')

        # Door and car data
        intGarageFeet = int(float(garageFeet))
        if(intGarageFeet < 2):
            f.write('<div style="font-size:60px;background-color:darkred;color:white;padding:10px;border:3px solid black">Garage Door is Open.</div>')
        elif(intGarageFeet >= 2 and intGarageFeet < 6):
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Garage Door is Closed. Not Empty.</div>')
        else:
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Garage Door is Closed. Empty.</div>')

        f.write('<br><br>')

        # Temp and distance output
        f.write('<div style="background-color:gray;color:white;padding:10px;border:3px solid black">')
        f.write('<div style="font-size:60px">Garage: ' + garageTemp + '&deg;F.</div>')
        f.write('<div style="font-size:40px">Garage: ' + garageFeet + ' ft. / ' + garageInches + ' in.</div>')
        #f.write('<div style="font-size:40px">Garage: ' + garageInches + ' in.</div>')
        f.write('</div>')
        f.write('<br><br>')

        # Ble1 data and Ble2 and Ble3 data
        intBle1Feet = int(float(ble1Feet))
        intBle2Feet = int(float(ble2Feet))
        intBle3Feet = int(float(ble3Feet))
        if(intBle1Feet > 0 and intBle1Feet <= 18):
            f.write('<div style="font-size:60px;background-color:darkred;color:white;padding:10px;border:3px solid black">Dotty is on Julia&#39;s bed!</div>')
        elif(intBle2Feet > 0 and intBle2Feet < 18):
            f.write('<div style="font-size:60px;background-color:darkblue;color:white;padding:10px;border:3px solid black">Dotty is on her bed!</div>')
        elif(intBle3Feet > 0 and intBle3Feet < 30):
            f.write('<div style="font-size:60px;background-color:darkblue;color:white;padding:10px;border:3px solid black">Dotty is in the living room!</div>')
        else:
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Dotty is not on a bed.</div>')

        f.write('<br><br>')

        lastTvRoomPayload = out
        lastTvRoomTime = time.strftime("%c")
        
    elif(dataPoints[0] == 'GARAGE'):
        garageFeet = dataPoints[2]
        garageInches = str(float(garageFeet) * 12)
        garageTemp = dataPoints[3]

        # pool data
        f.write('<div style="font-size:60px;background-color:blue;color:white;padding:10px;border:3px solid black">Pool: ' +poolTemp + '&deg;F - Box: ' + airTemp + '&deg;F</div>')
        f.write('<br><br>')

        # tvroom data
        f.write('<div style="font-size:60px;background-color:blue;color:white;padding:10px;border:3px solid black">TV Room: ' + tvRoomTemp + '&deg;F</div>')
        f.write('<br><br>')
        
        # Door and car data
        intGarageFeet = int(float(garageFeet))
        if(intGarageFeet < 2):
            f.write('<div style="font-size:60px;background-color:darkred;color:white;padding:10px;border:3px solid black">Garage Door is Open.</div>')
        elif(intGarageFeet >= 2 and intGarageFeet < 6):
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Garage Door is Closed. Not Empty.</div>')
        else:
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Garage Door is Closed. Empty.</div>')

        f.write('<br><br>')
                                
        # Temp and distance output
        f.write('<div style="background-color:gray;color:white;padding:10px;border:3px solid black">')
        f.write('<div style="font-size:60px">Garage: ' + garageTemp + '&deg;F.</div>')
        f.write('<div style="font-size:40px">Garage: ' + garageFeet + ' ft. / ' + garageInches + ' in.</div>')
        #f.write('<div style="font-size:40px">Garage: ' + garageInches + ' in.</div>')
        f.write('</div>')
        f.write('<br><br>')

        # Ble1 data and Ble2 and Ble3 data
        intBle1Feet = int(float(ble1Feet))
        intBle2Feet = int(float(ble2Feet))
        intBle3Feet = int(float(ble3Feet))
        if(intBle1Feet > 0 and intBle1Feet <= 18):
            f.write('<div style="font-size:60px;background-color:darkred;color:white;padding:10px;border:3px solid black">Dotty is on Julia&#39;s bed!</div>')
        elif(intBle2Feet > 0 and intBle2Feet < 18):
            f.write('<div style="font-size:60px;background-color:darkblue;color:white;padding:10px;border:3px solid black">Dotty is on her bed!</div>')
        elif(intBle3Feet > 0 and intBle3Feet < 30):
            f.write('<div style="font-size:60px;background-color:darkblue;color:white;padding:10px;border:3px solid black">Dotty is in the living room!</div>')    
        else:
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Dotty is not on a bed.</div>')

        f.write('<br><br>')

        lastGaragePayload = out
        lastGarageTime = time.strftime("%c")

    elif(dataPoints[0] == 'BLE1'):

        ble1Feet = dataPoints[2]

        # pool data
        f.write('<div style="font-size:60px;background-color:blue;color:white;padding:10px;border:3px solid black">Pool: ' +poolTemp + '&deg;F - Box: ' + airTemp + '&deg;F</div>')
        f.write('<br><br>')

	# tvroom data
        f.write('<div style="font-size:60px;background-color:blue;color:white;padding:10px;border:3px solid black">TV Room: ' + tvRoomTemp + '&deg;F</div>')
        f.write('<br><br>')
        
        # Door and car data
        intGarageFeet = int(float(garageFeet))
        if(intGarageFeet < 2):
            f.write('<div style="font-size:60px;background-color:darkred;color:white;padding:10px;border:3px solid black">Garage Door is Open.</div>')
        elif(intGarageFeet >= 2 and intGarageFeet < 6):
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Garage Door is Closed. Not Empty.</div>')
        else:
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Garage Door is Closed. Empty.</div>')

        f.write('<br><br>')
                                
        # Temp and distance output
        f.write('<div style="background-color:gray;color:white;padding:10px;border:3px solid black">')
        f.write('<div style="font-size:60px">Garage: ' + garageTemp + '&deg;F.</div>')
        f.write('<div style="font-size:40px">Garage: ' + garageFeet + ' ft. / ' + garageInches + ' in.</div>')
        #f.write('<div style="font-size:40px">Garage: ' + garageInches + ' in.</div>')
        f.write('</div>')
        f.write('<br><br>')

        # Ble1 data and Ble2 and Ble3 data
        intBle1Feet = int(float(ble1Feet))
        intBle2Feet = int(float(ble2Feet))
        intBle3Feet = int(float(ble3Feet))
        if(intBle1Feet > 0 and intBle1Feet <= 18):
            f.write('<div style="font-size:60px;background-color:darkred;color:white;padding:10px;border:3px solid black">Dotty is on Julia&#39;s bed!</div>')
        elif(intBle2Feet > 0 and intBle2Feet < 18):
            f.write('<div style="font-size:60px;background-color:darkblue;color:white;padding:10px;border:3px solid black">Dotty is on her bed!</div>')
        elif(intBle3Feet > 0 and intBle3Feet < 30):
            f.write('<div style="font-size:60px;background-color:darkblue;color:white;padding:10px;border:3px solid black">Dotty is in the living room!</div>')    
        else:
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Dotty is not on a bed.</div>')

        f.write('<br><br>')

        lastBle1Payload = out
        lastBle1Time = time.strftime("%c")

    elif(dataPoints[0] == 'BLE2'):

        ble2Feet = dataPoints[2]

        # pool data
        f.write('<div style="font-size:60px;background-color:blue;color:white;padding:10px;border:3px solid black">Pool: ' +poolTemp + '&deg;F - Box: ' + airTemp + '&deg;F</div>')
        f.write('<br><br>')

	# tvroom data
        f.write('<div style="font-size:60px;background-color:blue;color:white;padding:10px;border:3px solid black">TV Room: ' + tvRoomTemp + '&deg;F</div>')
        f.write('<br><br>')
        
        # Door and car data
        intGarageFeet = int(float(garageFeet))
        if(intGarageFeet < 2):
            f.write('<div style="font-size:60px;background-color:darkred;color:white;padding:10px;border:3px solid black">Garage Door is Open.</div>')
        elif(intGarageFeet >= 2 and intGarageFeet < 6):
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Garage Door is Closed. Not Empty.</div>')
        else:
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Garage Door is Closed. Empty.</div>')

        f.write('<br><br>')
                                
        # Temp and distance output
        f.write('<div style="background-color:gray;color:white;padding:10px;border:3px solid black">')
        f.write('<div style="font-size:60px">Garage: ' + garageTemp + '&deg;F.</div>')
        f.write('<div style="font-size:40px">Garage: ' + garageFeet + ' ft. / ' + garageInches + ' in.</div>')
        #f.write('<div style="font-size:40px">Garage: ' + garageInches + ' in.</div>')
        f.write('</div>')
        f.write('<br><br>')

        # Ble1 data and Ble2 and Ble3 data
        intBle1Feet = int(float(ble1Feet))
        intBle2Feet = int(float(ble2Feet))
        intBle3Feet = int(float(ble3Feet))
        if(intBle1Feet > 0 and intBle1Feet <= 18):
            f.write('<div style="font-size:60px;background-color:darkred;color:white;padding:10px;border:3px solid black">Dotty is on Julia&#39;s bed!</div>')
        elif(intBle2Feet > 0 and intBle2Feet < 18):
            f.write('<div style="font-size:60px;background-color:darkblue;color:white;padding:10px;border:3px solid black">Dotty is on her bed!</div>')
        elif(intBle3Feet > 0 and intBle3Feet < 30):
            f.write('<div style="font-size:60px;background-color:darkblue;color:white;padding:10px;border:3px solid black">Dotty is in the living room!</div>')    
        else:
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Dotty is not on a bed.</div>')

        f.write('<br><br>')

        lastBle2Payload = out
        lastBle2Time = time.strftime("%c")    

    elif(dataPoints[0] == 'BLE3'):

        ble3Feet = dataPoints[2]

        # pool data
        f.write('<div style="font-size:60px;background-color:blue;color:white;padding:10px;border:3px solid black">Pool: ' +poolTemp + '&deg;F - Box: ' + airTemp + '&deg;F</div>')
        f.write('<br><br>')

	# tvroom data
        f.write('<div style="font-size:60px;background-color:blue;color:white;padding:10px;border:3px solid black">TV Room: ' + tvRoomTemp + '&deg;F</div>')
        f.write('<br><br>')
        
        # Door and car data
        intGarageFeet = int(float(garageFeet))
        if(intGarageFeet < 2):
            f.write('<div style="font-size:60px;background-color:darkred;color:white;padding:10px;border:3px solid black">Garage Door is Open.</div>')
        elif(intGarageFeet >= 2 and intGarageFeet < 6):
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Garage Door is Closed. Not Empty.</div>')
        else:
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Garage Door is Closed. Empty.</div>')

        f.write('<br><br>')
                                
        # Temp and distance output
        f.write('<div style="background-color:gray;color:white;padding:10px;border:3px solid black">')
        f.write('<div style="font-size:60px">Garage: ' + garageTemp + '&deg;F.</div>')
        f.write('<div style="font-size:40px">Garage: ' + garageFeet + ' ft. / ' + garageInches + ' in.</div>')
        #f.write('<div style="font-size:40px">Garage: ' + garageInches + ' in.</div>')
        f.write('</div>')
        f.write('<br><br>')

        # Ble1 data and Ble2 and Ble3 data
        intBle1Feet = int(float(ble1Feet))
        intBle2Feet = int(float(ble2Feet))
        intBle3Feet = int(float(ble3Feet))
        if(intBle1Feet > 0 and intBle1Feet <= 18):
            f.write('<div style="font-size:60px;background-color:darkred;color:white;padding:10px;border:3px solid black">Dotty is on Julia&#39;s bed!</div>')
        elif(intBle2Feet > 0 and intBle2Feet < 18):
            f.write('<div style="font-size:60px;background-color:darkblue;color:white;padding:10px;border:3px solid black">Dotty is on her bed!</div>')
        elif(intBle3Feet > 0 and intBle3Feet < 30):
            f.write('<div style="font-size:60px;background-color:darkblue;color:white;padding:10px;border:3px solid black">Dotty is in the living room!</div>')    
        else:
            f.write('<div style="font-size:60px;background-color:green;color:white;padding:10px;border:3px solid black">Dotty is not on a bed.</div>')

        f.write('<br><br>')

        lastBle3Payload = out
        lastBle3Time = time.strftime("%c")  
        
    else:
        f.write('<div style="font-size:60px">Unknown Node:' + dataPoints[0] + '</div>')

    f.write('<div style="font-size:20px"><em>Last Pool Payload: ' + lastPoolPayload + ' @ ' + lastPoolTime + '</em></div>')
    f.write('<div style="font-size:20px"><em>Last Garage Payload: ' + lastGaragePayload + ' @ ' + lastGarageTime + '</em></div>')
    f.write('<div style="font-size:20px"><em>Last Ble1 Payload: ' + lastBle1Payload + ' @ ' + lastBle1Time + '</em></div>')
    f.write('<div style="font-size:20px"><em>Last Ble2 Payload: ' + lastBle2Payload + ' @ ' + lastBle2Time + '</em></div>')
    f.write('<div style="font-size:20px"><em>Last Ble3 Payload: ' + lastBle3Payload + ' @ ' + lastBle3Time + '</em></div>')
    f.write('<div style="font-size:20px"><em>Last TvRoom Payload: ' + lastTvRoomPayload + ' @ ' + lastTvRoomTime + '</em></div>')
    f.write('<br>')
    f.write('</body></html>')
    f.close()

    db = MySQLdb.connect("localhost", "pi", "piTin", "piHub")
    curs=db.cursor()

    try:
        curs.execute ("INSERT INTO payload (payload, created, node, dataPoints, data1, data2) values('" + out + "',NOW(),'" + dataPoints[0] + "', " + dataPoints[1] + ",'" + dataPoints[2] + "','" + dataPoints[3] + "');")
        db.commit()

    except Exception, e:
        print "Error again"
        print e
        db.rollback()
    
    time.sleep(1)
    
    
