import serial


class RCControl(object):

    def __init__(self, serial_port):
        self.serial_port = serial.Serial(serial_port, 9600)

    def steer(self, prediction):
        if prediction == 2:
            self.serial_port.write(chr(1).encode())
            print("Forward")
        elif prediction == 0:
            self.serial_port.write(chr(7).encode())
            print("Left")
        elif prediction == 1:
            self.serial_port.write(chr(6).encode())
            print("Right")
        else:
            self.stop()

    def stop(self):
        self.serial_port.write(chr(0).encode())
