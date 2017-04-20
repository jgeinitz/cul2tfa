#!/usr/bin/python

import time
import serial

verbose = 1

temperature = 0.0

def printYesNo(val):
    if val == 1:
        return "yes"
    else:
        return "no"
    
def checkcrc(telegram):
    return 1

def reportvalues():
    print "SensorID:    "+ str(sid)
    print "New battery: "+printYesNo(new_battery)
    print "low battery: "+printYesNo(lowbat)
    print "Temp:        "+ str(temperature)
    if hygro == 106:
        h="NaN"
    else:
        h=str(hygro)
    print "humidity:    "+h
    print'\n'

def reportvaluesLine():
    if hygro == 106:
        h="-1"
    else:
        h=str(hygro)
    x='sensorid:'+str(sid)+' newbat:'+str(new_battery)+ ' lowbat:'+str(lowbat)+' temp:'+str(temperature) + ' humidity:'+h
    print x
    

def tx29parse(telegram):
    global sid
    global new_battery
    global temperature
    global lowbat
    global hygro
    global crc

    if telegram[0:1] == '9':
        sid=int(telegram[1:2])*4 + ((int(telegram[2:3])&0xc)/4)
        if int(telegram[2:3])&2 :
            new_battery=1
        else:
            new_battery=0
        temperature = ( (float(telegram[3:4])*10) + float(telegram[4:5]) + (float(telegram[5:6])/10.0)) - 40
        if (int(telegram[6:7])&0x8) != 0:
            lowbat=1
        else:
            lowbat=0
        hygro= ((int(telegram[6:7])&0x7)<<4)+int(telegram[7:8],16)
        crc= (int(telegram[8:9],16)<<4)+int(telegram[9:10],16)
        return 1
    else:
        if verbose : print 'unknown length '+telegram[0:1]
        return 0
        
def culparse(telegram):
    if telegram.find('N02',0) == 0 :
        return tx29parse(telegram[3:13])
    else:
        if verbose: print 'Unknown CUL Telegram \''+telegram+'\''
    return 0

if verbose: print 'Interface between DENIC Weather Station and MySql\n'
if verbose: print 'Opening CUL connection\n'

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

if ser.isOpen():

    if verbose: print 'init CUL\n'
    ser.write('X0\r\nX21\r\nNr2\r\nV\r\n')


    running=1
    input=1
    while running == 1 :

        while ser.inWaiting() > 0:
            out = ser.readline()
            if verbose : print out
            if out != '':
                if culparse(out.rstrip('\n').rstrip('\r')):
                    if checkcrc(out.rstrip('\n').rstrip('\r')):
                        running=0
                        if ser.inWaiting() > 0 : running=1
                        if verbose: reportvalues()
			if sid != 14 : running = 1
        if running == 1:
            time.sleep(1)
else:
    running=0
reportvaluesLine()
if verbose : print "turning off receiver"
ser.write("Nx\r\nX00\r\n")
ser.close()
