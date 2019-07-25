#!/usr/bin/python3
# -*- coding=utf-8 -*-
# vim: expandtab  tabstop=4

from datetime import datetime
from socket import gethostname
import serial
import os
from time import sleep

HOSTNAME=gethostname()

def log_vaisala(data_root = '/aws_data'):
    today=datetime.utcnow().strftime('%Y-%m-%d')
    outfile=os.path.join(data_root,HOSTNAME+'-'+today+'.tsv')
    logfile=os.path.join(data_root,HOSTNAME+'-'+today+'.log')
    f = open(outfile,'a')#appends to existing file 
    g = open(logfile, 'a')
    try:
        ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=9600,
            timeout=60
        )

        while ser.isOpen():
            data = ser.read(3)
            datastring = ''.join([chr(b) for b in data])
            if (data_string == '0R0'):
                data2 = ser.readline()
                datastring2 = ''.join([chr(b) for b in data2])
                f.write(datetime.utcnow().isoformat() + ',' + datastring + datastring2) # \n is line separator
                f.flush()
            else:
                g.write(datetime.utcnow().isoformat() +' reconnecting no data \n')
                ser.close() #so it exits the While loop
                f.close()
                g.close()
                
            if not today == datetime.utcnow().strftime('%Y-%m-%d'): #i.e. it is tomorrow
                ser.close() # leave lower while loop, rename output file

    except (serial.SerialException, OSError):
        d = datetime.utcnow()
        g.write(d.isoformat() +' reconnecting SerialException\n')
        g.flush()
        sleep(10)

    return 
    
if __name__ == "__main__":
    #i.e. if file run directly
    while True:
        #run continuously
        log_vaisala()

