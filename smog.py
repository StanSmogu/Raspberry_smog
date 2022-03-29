START=0xFA
STOP1=0x0D
STOP2=0x0A

import serial
import time
import threading
import mysql.connector
import datetime

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.output(21, GPIO.LOW)
GPIO.output(20, GPIO.LOW)
GPIO.output(16, GPIO.LOW)

ids=3

global ser
global UART


UART=serial.Serial('/dev/ttyUSB0',9600,8,'N',1,0)


def insert_live(ozone,no2,co2,pm25,pm10, temp,wind_d,wind_s,wind_g,ozone_temperature,ozone_humidity,no2_temperature,no2_humidity):


    try:
        mydb = mysql.connector.connect(host="79.189.200.10",port="3400",user="meteo_zam",passwd="2&X(jX]l@R$0=]4",database="meteo_zam")
        mycursor=mydb.cursor()
        #print (database_live)
        sql = "INSERT INTO measure_live (ids,ozone,no2,co2,pm2_5, pm10,temperature,wind_direction,wind_speed,wind_gust,ozone_temperature,ozone_humidity,no2_temperature,no2_humidity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (ids,ozone,no2,co2,pm25,pm10, temp,wind_d,wind_s,wind_g,ozone_temperature,ozone_humidity,no2_temperature,no2_humidity)
        mycursor.execute(sql, val)
        mydb.commit()
        
        now = datetime.datetime.now()
        print(now)

        print(mycursor.rowcount, " new live record inserted.")
    except mysql.connector.Error as e:
        print ("Error code:", e.errno)        # error number
        print ("SQLSTATE value:", e.sqlstate) # SQLSTATE value
        print ("Error message:", e.msg )      # error message
        print ("Error:", e)                # errno, sqlstate, msg values
        s = str(e)
        print ("Error:", s)                  # errno, sqlstate, msg values


def update_technical(error__vent,error_ozone_sensor,error_no2_sensor,heater,reserve):

    try:
        mydb = mysql.connector.connect(host="79.189.200.10",port="3400",user="meteo_zam",passwd="2&X(jX]l@R$0=]4",database="meteo_zam")
        mycursor=mydb.cursor()
        #print (database_live)
        sql = "UPDATE errors SET vent = %s,ozone=%s,no2=%s,heater=%s,reserve=%s  WHERE ids = %s"
        val = (error__vent,error_ozone_sensor,error_no2_sensor,heater,reserve,ids)
        mycursor.execute(sql, val)
        mydb.commit()

        print(mycursor.rowcount, " record updated.")
    except mysql.connector.Error as e:
        print ("Error code:", e.errno)        # error number
        print ("SQLSTATE value:", e.sqlstate) # SQLSTATE value
        print ("Error message:", e.msg )      # error message
        print ("Error:", e)                # errno, sqlstate, msg values
        s = str(e)
        print ("Error:", s)                  # errno, sqlstate, msg values

def delete_old():

    try:
        mydb = mysql.connector.connect(host="79.189.200.10",port="3400",user="meteo_zam",passwd="2&X(jX]l@R$0=]4",database="meteo_zam")
        mycursor=mydb.cursor()
        sql = "DELETE FROM measure_live WHERE ids = 3 AND measure_date < DATE_SUB(NOW(),INTERVAL 2 hour)"
        val = (ids)
        mycursor.execute(sql,val)
        mydb.commit()

        print(mycursor.rowcount, " record deleated.")
    except mysql.connector.Error as e:
        print ("Error code:", e.errno)        # error number
        print ("SQLSTATE value:", e.sqlstate) # SQLSTATE value
        print ("Error message:", e.msg )      # error message
        print ("Error:", e)                # errno, sqlstate, msg values
        s = str(e)
        print ("Error:", s)                  # errno, sqlstate, msg values

def diode_color(ozone,no2,co2,pm25,pm10):
    if pm10<=50:
        #dioda 1
        GPIO.output(21, GPIO.HIGH)
        GPIO.output(20, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
    elif pm10>50 and pm10<=110:
        #dioda2
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(16, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
    elif pm10>110:
        #dioda3
        GPIO.output(16, GPIO.HIGH)
        GPIO.output(20, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)

def measure():
    sensor_error=1
    ozone_old=0
    no2_old=0
    while (True):
        
        s=''
        c=0
        c=UART.inWaiting()
        data=[]
        
        if c:
            s=UART.read(c)
            #print(s)
            for i in range (0,len(s)):
                data.append(chr(s[i]))
            if (len(data)==52):
                start=data[0]
                stop1=data[50]
                stop2=data[51]
                if (start==chr(START)):
                    if (stop1+stop2==chr(STOP1)+chr(STOP2)):
                        #print ("Odebrano ramke")
                        #print (data[4])
                        #ozone_data=data[1]+data[2]+data[3]+data[4]
                        ozone_data=data[10]+data[11]+data[12]+data[13]
                        try:
                            ozone = int(ozone_data)
                        except ValueError:
                            ozone=None
                        
                        ozone_temperature_data=data[5]+data[6]+data[7]
                        try:
                            ozone_temperature = float(ozone_temperature_data)
                        except ValueError:
                            ozone_temperature=None
                        
                        ozone_humidity_data=data[8]+data[9]
                        try:
                            ozone_humidity = int(ozone_humidity_data)
                        except ValueError:
                            ozone_humidity=None
                        
                        #no2_data=data[10]+data[11]+data[12]+data[13]
                        no2_data=data[1]+data[2]+data[3]+data[4]
                        try:
                            no2 = int(no2_data)
                        except ValueError:
                            no2=None
                        
                        no2_temperature_data=data[14]+data[15]+data[16]
                        try:
                            no2_temperature = float(no2_temperature_data)
                        except ValueError:
                            no2_temperature=None
                        
                        no2_humidity_data=data[17]+data[18]
                        try:
                            no2_humidity = int(no2_humidity_data)
                        except ValueError:
                            no2_humidity=None
                        
                        co2_data=data[19]+data[20]+data[21]+data[22]
                        try:
                            co2 = int(co2_data)
                        except ValueError:
                            co2=None
                        
                        pm25_data=data[23]+data[24]+data[25]+data[26]
                        try:
                            pm25 = int(pm25_data)
                        except ValueError:
                            pm25=None
                        
                        pm10_data=data[27]+data[28]+data[29]+data[30]
                        try:
                            pm10 = int(pm10_data)
                        except ValueError:
                            pm10=None
                        
                        temp_data=data[31]+data[32]+data[33]+'.'+data[34]
                        try:
                            temp = float(temp_data)
                        except ValueError:
                            temp=None
                        
                        wind_d_data=data[35]
                        try:
                            wind_d = int(wind_d_data)
                        except ValueError:
                            wind_d=None
                        
                        wind_s_data=data[36]+data[37]+data[38]
                        try:
                            wind_s = int(wind_s_data)
                        except ValueError:
                            wind_s=None
                        
                        wind_g_data=data[39]+data[40]+data[41]
                        try:
                            wind_g = int(wind_g_data)
                        except ValueError:
                            wind_g=None
                        
                        error_vent_data=data[42]
                        try:
                            error_vent = int(error_vent_data)
                        except ValueError:
                            error_vent=None
                        
                        #error_ozone_sensor_data=data[43]
                        error_ozone_sensor_data=data[44]
                        try:
                            error_ozone_sensor = int(error_ozone_sensor_data)
                        except ValueError:
                            error_ozone_sensor=None
                        
                        #error_no2_sensor_data=data[44]
                        error_no2_sensor_data=data[43]
                        try:
                            error_no2_sensor = int(error_no2_sensor_data)
                        except ValueError:
                            error_no2_sensor=None
                        
                        heater_data=data[45]
                        try:
                            heater = int(heater_data)
                        except ValueError:
                            heater=None
                        
                        reserve_data=data[46]
                        try:
                            reserve = int(reserve_data)
                        except ValueError:
                            reserve=None
                        
                        cr_data=data[47]+data[48]+data[49]
                        try:
                            cr = int(cr_data)
                        except ValueError:
                            cr=None
                        
                        if (error_ozone_sensor==sensor_error):
                            ozone=None
                            
                        if (error_no2_sensor==sensor_error):
                            no2=None
                        
                        if ozone is not None and (ozone >1000 or ozone <1):
                            ozone=None
                        
                        if no2 is not None and (no2 >1000 or no2 <1):
                            no2=None
                            
                        if pm25 is not None and (pm25 >1000 or pm25 <1):
                            pm25=None
                            
                        if pm10 is not None and (pm10 >1000 or pm10 <1):
                            pm10=None
                        
                        insert_live(ozone,no2,co2,pm25,pm10,temp,wind_d,wind_s,wind_g,ozone_temperature,ozone_humidity,no2_temperature,no2_humidity)
                        update_technical(error_vent,error_ozone_sensor,error_no2_sensor,heater,reserve)
                        delete_old()
                        diode_color(ozone,no2,co2,pm25,pm10)
                        
        time.sleep(1)


measure()
    

    
