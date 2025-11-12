'''
 *   Copyright (C) 2016 Alex Koren
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program; if not, write to the Free Software
 *   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
'''
import os
import sys
import re

import time
import serial


e = b"\xff\xff\xff"

def getBaudrate(ser, fSize=None, checkModel=None):
    for baudrate in (115200, 2400, 4800, 9600, 19200, 38400, 57600):

        ser.baudrate = baudrate
        ser.timeout = 3000 / baudrate + .2
        print('Trying with baudrate: ' + str(baudrate) + '...')
        ser.write(b"\xff\xff\xff")
        ser.write(b'connect')
        ser.write(b"\xff\xff\xff")
        r = ser.read(128)
        if b'comok' in r:
            print('Connected with baudrate: ' + str(baudrate) + '...')
            
            # Parse the response before changing baudrate
            status, _unknown1, model, fwversion, mcucode, serial_num, flashSize = r.strip(b"\xff\x00").split(b',')
            status = status.decode('ascii')
            model = model.decode('ascii')
            fwversion = fwversion.decode('ascii')
            mcucode = mcucode.decode('ascii')
            serial_num = serial_num.decode('ascii')
            flashSize = int(flashSize.decode('ascii'))
            print('Status: ' + status.split(' ')[0])
            if status.split(' ')[1] == "1":
                print('Touchscreen: yes')
            else:
                print('Touchscreen: no')
            print('Model: ' + model)
            print('Firmware version: ' + fwversion)
            print('MCU code: ' + mcucode)
            print('Serial: ' + serial_num)
            print('Flash size: ' + str(flashSize))
            
            # Change baudrate to 115200 if not already at that speed
            if baudrate != 115200:
                ser.write(b'bauds=115200' + b"\xff\xff\xff")
                time.sleep(0.1)
                ser.baudrate = 115200
                ser.timeout = 3000 / 115200 + .2
            
            if fSize and fSize > flashSize:
                print('File too big!')
                return False
            if checkModel and not checkModel in model:
                print('Wrong Display!')
                return False
            return True
    return False

def setDownloadBaudrate(ser, fSize, baudrate):
    ser.write(b"")
    ser.write(b"whmi-wri " + str(fSize).encode('ascii') + b"," + str(baudrate).encode('ascii') + b",0" + e)
    time.sleep(.05)
    ser.baudrate = baudrate
    ser.timeout = .5
    r = ser.read(1)
    if b"\x05" in r:
        return True
    return False

def transferFile(ser, filename, fSize):
    with open(filename, 'rb') as hmif:
        dcount = 0
        while True:
            data = hmif.read(4096)
            if len(data) == 0:
                break
            dcount += len(data)
            ser.timeout = 5
            ser.write(data)
            sys.stdout.write('\rDownloading, %3.1f%%...'% (dcount / float(fSize) * 100.0))
            sys.stdout.flush()
            ser.timeout = .5
            time.sleep(.5)
            r = ser.read(1)
            if b"\x05" in r:
                continue
            else:
                print()
                return False
        print()
    return True

def upload(ser, filename, checkModel=None):
    if not getBaudrate(ser, os.path.getsize(filename), checkModel):
        print('Could not find baudrate')
        exit(1)

    if not setDownloadBaudrate(ser, os.path.getsize(filename), 115200):
        print('Could not set download baudrate')
        exit(1)

    if not transferFile(ser, filename, os.path.getsize(filename)):
        print('Could not transfer file')
        exit(1)

    print('File transferred successfully')
    exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 4 and len(sys.argv) != 3:
        print('usage:\npython nextion.py file_to_upload.tft /path/to/dev/ttyDevice [nextion_model_name]\
        \nexample: nextion.py newUI.tft /dev/ttyUSB0 NX3224T024\
        \nnote: model name is optional')
        exit(1)

    try:
        serial_port = serial.Serial(sys.argv[2], 9600, timeout=5)
    except serial.SerialException:
        print('could not open serial device ' + sys.argv[2])
        exit(1)
    
    if not serial_port.is_open:
        serial_port.open()

    model_to_check = None
    if len(sys.argv) == 4:
        model_to_check = sys.argv[3]
        pattern = re.compile(r"^NX\d{4}[TK]\d{3}$")
        if not pattern.match(model_to_check):
            print('Invalid model name. Please give a correct one (e.g. NX3224T024)')
            exit(1)
    upload(serial_port, sys.argv[1], model_to_check)
