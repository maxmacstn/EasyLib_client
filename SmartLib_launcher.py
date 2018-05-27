import SmartLibrary_client
import serial.tools.list_ports
import sys
import glob
import cv2

CAM = 5

def connectRFID():
    print("Discovering RFID Scanner device")
    serialResult = find_RFID_ports()
    if (len(serialResult) == 0):
        # print("No devices found")
        return False
    else:
        return find_RFID_ports()[0]



def find_RFID_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port=port,baudrate=9600, timeout=2)
            response = s.readline().decode('utf-8').strip()
            if(response== "RFID Reader is ready.."):
                result.append(port)
                s.close()
                break
            s.close()
        except (OSError, serial.SerialException):
            pass

    return result

def connectCamera():
    cv2.VideoCapture(CAM)

if __name__ == '__main__':
    print("--- Launching application ---")
    serial = connectRFID()
    if(not serial):
        print("Error connecting to serial RFID Scanner")
    else:
        print("Connected to RFID Sensor at " + serial)
    SmartLibrary_client.launch(0, serial)


