import serial 
import re
import time
import serial.tools.list_ports
import serial




def get_com_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'USB Serial Port' in p.description:
            com = re.findall(r'COM\d+', p.description)
            return com[0]    
           
COM = get_com_port()
ser = serial.Serial(COM,
                    baudrate=921600,
                    timeout=1,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS)
output = str(int(time.time()))
fileName = output +'.txt'

def main():
    while True:
        rawdata = (ser.readline().decode('ascii'))
        
        if r'Frame :' in rawdata:
            tsp = time.time()
            tsp = str(int(round(tsp * 1000)))
            rawdata = rawdata +'TimeStamp:'+ tsp
            a =1
        print(rawdata)
        with open(fileName, 'a+') as f:
            f.write(rawdata)
        
if __name__ == '__main__':
    main()

