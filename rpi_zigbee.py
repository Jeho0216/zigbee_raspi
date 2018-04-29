import serial, sys


xbee = serial.Serial('/dev/ttyUSB0', 9600)
string = 'Hello from Raspberry Pi'
print ('Sending %s' %string)
xbee.write('Hello from Raspberry Pi')

type = 1
data = 0
under = 0
data_under = 0
data_type = 0
data_value = 0

try:
    while True:
        obj = xbee.readline()
        for i in obj:
            if ('0' <= i <= '9') & (type == 1) :
                data_type = data_type*10 + int(i)
            if ('0' <= i <= '9') & (data == 1) :
                if(under == 1):
                    data_under = data_under*10 + int(i)
                else:
                    data_value = data_value*10 + int(i)
            if i == ',':
                type = 0
                data = 1
            if i == '.':
                under = 1
                data_value = str(data_value) + '.'
            if i == ';':
                type = 1
                data = 0
                under = 0
                if data_under != 0:
                    data_value += str(data_under)
                print("data_type : " + str(data_type))
                print("data_value : " + str(data_value))
                data_type = 0
                data_value = 0
                data_under = 0

except KeyboardInterrupt:
    xbee.write('Bye from Raspberry Pi')
    xbee.close()

