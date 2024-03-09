import serial
import time

class SerialCom:
    def __init__(self, port='/dev/ttyACM0', baud_rate=19200):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = None
    
    def open_connection(self):
        try:
            self.ser = serial.Serial(self.port, self.baud_rate)
            print("Serial connection opened successfully.")
        except serial.SerialException as e:
            print("Error opening serial connection:", e)
    
    def read_data(self):
        if self.ser:
            try:
                data = self.ser.readline().decode().strip()
                return data
            except serial.SerialException as e:
                print("Error reading data:", e)
                return None
        else:
            print("Serial connection not open.")
    
    def write_data(self, message):
        if self.ser:
            try:
                self.ser.write(message.encode())
                print("Message sent:", message)
            except serial.SerialException as e:
                print("Error writing data:", e)
        else:
            print("Serial connection not open.")
    
    def close_connection(self):
        if self.ser:
            self.ser.close()
            print("Serial connection closed.")
        else:
            print("Serial connection not open.")



if __name__ == '__main__':

    serial_com = SerialCom()

    # Open the serial connection
    serial_com.open_connection()

    # Read data
    # data = serial_com.read_data()
    # print("Received data:", data)

    angle = 0

    while True:
        # Write data
        angle = angle + 5

        if angle > 20:
            angle = -20

        serial_com.ser.reset_output_buffer()
        serial_com.ser.reset_input_buffer()

        message = f"#2:{angle};;\r\n"
        serial_com.write_data(message)
        print("Saljem poruku: message")

        time.sleep(2)

        

    # Close the serial connection
    serial_com.close_connection()
