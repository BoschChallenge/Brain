# # -*- coding: utf-8 -*-import serial
import time
import binascii
import serial

class SerialHandler:
    def __init__(self, port='/dev/ttyUSB0', baud_rate=115200):
        self.serial = serial.Serial(port, baud_rate)
        if self.serial.isOpen():
            print("Serial connection opened successfully")
        else:
            print("Failed to open serial connection")

    def __del__(self):
        if self.serial.isOpen():
            self.serial.close()
            print("Serial connection closed")

    def cl(self, a):
        dat1 = a[0:1]

        if dat1 == 'a':
            dat1 = 10
        elif dat1 == 'b':
            dat1 = 11
        elif dat1 == 'c':
            dat1 = 12
        elif dat1 == 'd':
            dat1 = 13
        elif dat1 == 'e':
            dat1 = 14
        elif dat1 == 'f':
            dat1 = 15
            
        return dat1

    def read_data(self):
        time.sleep(0.1) 
        num = self.serial.inWaiting()
        if num: 
            try:   
                data = str(binascii.b2a_hex(self.serial.read(num)))
                if(len(data) > 8):
                    dat1 = data[6:7]
                    dat2 = data[7:8]
                    dat3 = data[8:9]
                    dat4 = data[9:10]
                    jl = (((int(self.cl(dat1)) * 16) + int(self.cl(dat2))) * 256) + ((int(self.cl(dat3)) * 16) + int(self.cl(dat4)))
                    return jl
            except Exception as e:
                print("Error reading data:", e)
                return None

def main():
    # Instantiate SerialHandler
    serial_handler = SerialHandler()

    while True:
        # Read data
        jl = serial_handler.read_data()
        if jl is not None:
            print("Received data:", jl)

if __name__ == "__main__":
    main()
