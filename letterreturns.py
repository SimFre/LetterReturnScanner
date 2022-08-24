#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timezone
import serial
# import time
import pysftp

# sudo pip3 install pyserial pysftp

# SERIAL_PORT = "COM13"
SERIAL_PORT = "/dev/ttyACM0"
SERIAL_BAUD = 9600
BACKUP_PATH = "backups"
SFTP_HOSTNAME = "ftp.example.com"
SFTP_USERNAME = "UserUserUser"
SFTP_PASSWORD = "PassPassPass"
SFTP_PATH = "/"


def sendData(buffer):
    timestamp = datetime.now(timezone.utc)
    timeformat = timestamp.strftime('%Y%m%d%H%M%S%fZ')
    filename = f"returns_{timeformat}.txt"

    localfolder = BACKUP_PATH + os.sep + timestamp.strftime('%Y'+os.sep+'%m')
    localfile = localfolder + os.sep + filename
    if os.makedirs(localfolder, exist_ok=True):
        print(f"Created {localfolder}")

    fp = open(localfile, "a")
    if fp.write(buffer) > 0:
        print(f"Successfully wrote to {localfile}")
    fp.close()

    with pysftp.Connection(host=SFTP_HOSTNAME, username=SFTP_USERNAME, password=SFTP_PASSWORD) as sftp:
        print("Established SFTP Connection.")
        sftp.put(localfile, filename + ".tmp")
        print(f"Sent {filename}.tmp")
        sftp.rename(filename + ".tmp", filename)
        print(f"Renamed file to {filename}")


if __name__ == '__main__':
    try:
        ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=0.3)  # ttyACM1 for Arduino board
        print("Starting up")
        connected = False
        commandToSend = 1  # get the distance in mm
        readOut = ""
        dataBuffer = ""
        idleCounter = 0
        while True:
            try:
                try:
                    readOut = ser.readline().decode('ascii').strip()
                except UnicodeDecodeError as ex:
                    print("ERROR!")
                    print(ex)
                    readOut = ""

                if len(readOut) > 0:
                    print(f"\nGot data: {readOut}")
                    dataBuffer += readOut + "\n"
                    idleCounter = 0
                    # ser.flush()  # flush the buffer

                else:
                    if idleCounter == 0:
                        print("Waiting", end=".")
                    elif idleCounter % 100 == 0:
                        print("\n", end=".")
                    else:
                        print("", end=".")
                    idleCounter = idleCounter + 1

                if idleCounter >= 90 and len(dataBuffer) > 0:
                    print(f"\nSend data to SFTP after {idleCounter} tries")
                    print(dataBuffer)
                    sendData(dataBuffer)
                    dataBuffer = ""
                    idleCounter = 0

                # time.sleep(0.1)

            except serial.SerialException:
                pass
    except serial.SerialException as ex:
        print(ex)
        sys.exit(1)
