import serial, sys
import mysql.connector

cnn = mysql.connector.connect(user='root', password='magic0426', host='127.0.0.1', database='project')
cursor = cnn.cursor()

add_temp = ("insert into temperature (device_num, temp) values(%s, %s)")
add_humi = ("insert into humidity (device_num, humi) values(%s, %s)")

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

                data_value += str(data_under)
                print("data_type : " + str(data_type))
                print("data_value : " + str(data_value))
                
                if data_type == 1:
                    cursor.execute(add_temp, (1, data_value))
                    print("temperature insert complete\n")
                elif data_type == 2:
                    cursor.execute(add_humi, (1, data_value))
                    print("humidity insert complete\n")
                
                data_type = 0
                data_value = 0
                data_under = 0
                cnn.commit()

except KeyboardInterrupt:
    xbee.write('Bye from Raspberry Pi')
    xbee.close()

