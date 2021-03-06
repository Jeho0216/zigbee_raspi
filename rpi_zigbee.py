import serial, sys
import MySQLdb

#connect to the DB
cnn = MySQLdb.connect("127.0.0.1", "homestead", "secret", "myapp")
cursor = cnn.cursor()

#executable SQL Query.
add_temp = ("insert into temperature (device_num, temp, time) values(%s, %s, now())")
add_humi = ("insert into humidity (device_num, humi, time) values(%s, %s, now())")

#Serial Communication start
xbee = serial.Serial('/dev/ttyUSB0', 9600)

string = 'Hello from Raspberry Pi'
print ('Sending %s' %string)
xbee.write('Hello from Raspberry Pi')

def getData(str_data):
    #select data to read.
    type = 1
    data = 0
    under = 0
    #read complete data
    data_under = 0
    data_type = 0
    data_value = 0
    
    for i in str_data:
        if('0' <= i <= '9') & (type == 1):
            data_type = data_type*10 + int(i)
        if('0' <= i <= '9') & (data == 1):
            if(under == 1):
                data_under = (data_under*10) + int(i)
            else:
                data_value = (data_value*10) + int(i)
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

            data_value = str(data_value) + str(data_under)
            print("data_type : " + str(data_type))
            print("data_value : " + str(data_value))
            #save data to DB
            insertDB(data_type, data_value)

            data_under = 0
            data_type = 0
            data_value = 0

def insertDB(insert_type, insert_val):
    if insert_type == 1:
        cursor.execute(add_temp, (1, insert_val))
        print("temperature insert complete\n")
    elif insert_type == 2:
        cursor.execute(add_humi, (1, insert_val))
        print("humidity insert complete\n")


try:
    while True:
        if xbee.in_waiting:
            obj = xbee.readline()
            #get data from obj.
            getData(obj)
            
            data_value = 0
            data_under = 0
            cnn.commit()
            xbee.flushInput()

except KeyboardInterrupt:
    xbee.write('Bye from Raspberry Pi')
    xbee.close()
