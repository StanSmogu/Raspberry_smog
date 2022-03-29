START=0xFA
STOP1=0x0D
STOP2=0x0A

import serial
import time
import threading
import mysql.connector
import datetime
from datetime import timedelta
import requests

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
is_ozone=False
is_no2=False
is_co2=False
is_pm25=False
is_pm10=False
is_temp=False
is_wind=False

data_time_min=0
data_time_min1=0
data_time_min2=0

     
UART=serial.Serial('/dev/ttyUSB0',9600,8,'N',1,0)

def ovr_air_quality(ozone,no2,co2,pm25,pm10):
    try:
        mydb = mysql.connector.connect(host="79.189.200.10",port="3400",user="meteo_zam",passwd="2&X(jX]l@R$0=]4",database="meteo_zam")
        
        mycursor=mydb.cursor()
        mycursor.execute("SELECT * FROM standards")
        standards = mycursor.fetchone()

        bdb_db_ozone=standards[20]
        db_um_ozone=standards[21]
        um_do_ozone=standards[22]
        do_zl_ozone=standards[23]
        zl_bzl_ozone=standards[24]
        
        bdb_db_no2=standards[25]
        db_um_no2=standards[26]
        um_do_no2=standards[27]
        do_zl_no2=standards[28]
        zl_bzl_no2=standards[29]
        
        bdb_db_co2=standards[30]
        db_um_co2=standards[31]
        um_do_co2=standards[32]
        do_zl_co2=standards[33]
        zl_bzl_co2=standards[34]
        
        bdb_db_pm25=standards[35]
        db_um_pm25=standards[36]
        um_do_pm25=standards[37]
        do_zl_pm25=standards[38]
        zl_bzl_pm25=standards[39]
        
        bdb_db_pm10=standards[40]
        db_um_pm10=standards[41]
        um_do_pm10=standards[42]
        do_zl_pm10=standards[43]
        zl_bzl_pm10=standards[44]
    except mysql.connector.Error as e:
        print ("Error code:", e.errno)        # error number
        print ("SQLSTATE value:", e.sqlstate) # SQLSTATE value
        print ("Error message:", e.msg )      # error message
        print ("Error:", e)                # errno, sqlstate, msg values
        s = str(e)
        print ("Error:", s)                  # errno, sqlstate, msg values
    
    if ozone is not None:
        if ozone <= bdb_db_ozone:
            ozone_ovr=6
        elif ozone > bdb_db_ozone and ozone <= db_um_ozone:
            ozone_ovr=5
        elif ozone > db_um_ozone and ozone <= um_do_ozone:
            ozone_ovr=4
        elif ozone > um_do_ozone and ozone <= do_zl_ozone:
            ozone_ovr=3
        elif ozone > do_zl_ozone and ozone <= zl_bzl_ozone:
            ozone_ovr=2
        elif ozone > zl_bzl_ozone:
            ozone_ovr=1
        else:
            ozone_ovr=404
    else:
        ozone_ovr=404
    
    if no2 is not None:
        if no2 <= bdb_db_no2:
            no2_ovr=6
        elif no2 > bdb_db_no2 and no2 <= db_um_no2:
            no2_ovr=5
        elif no2 > db_um_no2 and no2 <= um_do_no2:
            no2_ovr=4
        elif no2 > um_do_no2 and no2 <= do_zl_no2:
            no2_ovr=3
        elif no2 > do_zl_no2 and no2 <= zl_bzl_no2:
            no2_ovr=2
        elif no2 > zl_bzl_no2:
            no2_ovr=1
        else:
            no2_ovr=404
    else:
        no2_ovr=404
    
    if co2 is not None:
        if co2 <= bdb_db_co2:
            co2_ovr=6
        elif co2 > bdb_db_co2 and co2 <= db_um_co2:
            co2_ovr=5
        elif co2 > db_um_co2 and co2 <= um_do_co2:
            co2_ovr=4
        elif co2 > um_do_co2 and co2 <= do_zl_co2:
            co2_ovr=3
        elif co2 > do_zl_co2 and co2 <= zl_bzl_co2:
            co2_ovr=2
        elif co2 > zl_bzl_co2:
            co2_ovr=1
        else:
            co2_ovr=404
    else:
        co2_ovr=404
    
    if pm25 is not None:
        if pm25 <= bdb_db_pm25:
            pm25_ovr=6
        elif pm25 > bdb_db_pm25 and pm25 <= db_um_pm25:
            pm25_ovr=5
        elif pm25 > db_um_pm25 and pm25 <= um_do_pm25:
            pm25_ovr=4
        elif pm25 > um_do_pm25 and pm25 <= do_zl_pm25:
            pm25_ovr=3
        elif pm25 > do_zl_pm25 and pm25 <= zl_bzl_pm25:
            pm25_ovr=2
        elif pm25 > zl_bzl_pm25:
            pm25_ovr=1
        else:
            pm25_ovr=404
    else:
        pm25_ovr=404
    
    if pm10 is not None:
        if pm10 <= bdb_db_pm10:
            pm10_ovr=6
        elif pm10 > bdb_db_pm10 and pm10 <= db_um_pm10:
            pm10_ovr=5
        elif pm10 > db_um_pm10 and pm10 <= um_do_pm10:
            pm10_ovr=4
        elif pm10 > um_do_pm10 and pm10 <= do_zl_pm10:
            pm10_ovr=3
        elif pm10 > do_zl_pm10 and pm10 <= zl_bzl_pm10:
            pm10_ovr=2
        elif pm10 > zl_bzl_pm10:
            pm10_ovr=1
        else:
            pm10_ovr=404
    else:
        pm10_ovr=404
    ozone_ovr=404
    ovr_list=[ozone_ovr,no2_ovr,co2_ovr,pm25_ovr,pm10_ovr]
    overall=min(ovr_list)
    if overall is 404:
        overall=None
    diode_color(overall)
    return overall

def database(sql,val):
    try:
        mydb = mysql.connector.connect(host="79.189.200.10",port="3400",user="meteo_zam",passwd="2&X(jX]l@R$0=]4",database="meteo_zam")
        mycursor=mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()
        
        now = datetime.datetime.now()
        print(now)

        print(mycursor.rowcount," record done.")
    except mysql.connector.Error as e:
        print ("Error code:", e.errno)        # error number
        print ("SQLSTATE value:", e.sqlstate) # SQLSTATE value
        print ("Error message:", e.msg )      # error message
        print ("Error:", e)                # errno, sqlstate, msg values
        s = str(e)
        print ("Error:", s)                  # errno, sqlstate, msg values



def insert_live(ozone,no2,co2,pm25,pm10, temp,wind_d,wind_s,wind_g,ozone_temperature,ozone_humidity,no2_temperature,no2_humidity,air_quality):
    sql = "INSERT INTO measure_live (ids,ozone,no2,co2,pm2_5, pm10,temperature,wind_direction,wind_speed,wind_gust,ozone_temperature,ozone_humidity,no2_temperature,no2_humidity,air_quality) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (ids,ozone,no2,co2,pm25,pm10, temp,wind_d,wind_s,wind_g,ozone_temperature,ozone_humidity,no2_temperature,no2_humidity,air_quality)
        
    database(sql,val)

def update_technical(error__vent,error_ozone_sensor,error_no2_sensor,heater,reserve):

    sql = "UPDATE errors SET vent = %s,ozone=%s,no2=%s,heater=%s,reserve=%s  WHERE ids = %s"
    val = (error__vent,error_ozone_sensor,error_no2_sensor,heater,reserve,ids)
    
    database(sql,val)

def delete_old():

    hours=2
    sql = "DELETE FROM measure_live WHERE ids = %s AND measure_date < DATE_SUB(NOW(),INTERVAL %s hour)"
    val = (ids,hours)
    
    database(sql,val)
    
def diode_color(overall):
    if overall is 6 or overall is 5:
        #zielone
        GPIO.output(21, GPIO.HIGH)
        GPIO.output(20, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
    elif overall is 4 or overall is 3:
        #żółte
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(16, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
    elif overall is 2 or overall is 1:
        #czerwone
        GPIO.output(16, GPIO.HIGH)
        GPIO.output(20, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
    
def network_connection():
    try:
        x=requests.get('https://google.com')
        connection=True
    except:
        connection=False
    return connection
    
def measure():
    
    try:
        mydb = mysql.connector.connect(host="79.189.200.10",port="3400",user="meteo_zam",passwd="2&X(jX]l@R$0=]4",database="meteo_zam") 
        mycursor=mydb.cursor()
        mycursor.execute("SELECT ozone,no2,co2,pm25,pm10,temp,wind FROM sensors WHERE ids="+str(ids))
        myresult = mycursor.fetchall()

        for x in myresult:
            is2_ozone=x[0]
            is2_no2=x[1]
            is2_co2=x[2]
            is2_pm25=x[3]
            is2_pm10=x[4]
            is2_temp=x[5]
            is2_wind=x[6]
    except mysql.connector.Error as e:
        print ("Error code:", e.errno)        # error number
        print ("SQLSTATE value:", e.sqlstate) # SQLSTATE value
        print ("Error message:", e.msg )      # error message
        print ("Error:", e)                # errno, sqlstate, msg values
        s = str(e)
        print ("Error:", s)                  # errno, sqlstate, msg values
    
    if (is2_ozone==1):
        is_ozone=True
    else:
        is_ozone=False
    
    if (is2_no2==1):
        is_no2=True
    else:
        is_no2=False
        
    if (is2_co2==1):
        is_co2=True
    else:
        is_co2=False
    
    if (is2_pm25==1):
        is_pm25=True
    else:
        is_pm25=False
    
    if (is2_pm10==1):
        is_pm10=True
    else:
        is_pm10=False
    
    if (is2_temp==1):
        is_temp=True
    else:
        is_temp=False
        
    if (is2_wind==1):
        is_wind=True
    else:
        is_wind=False
    
    
    
    sensor_error=1
    ozone_old=0
    no2_old=0
    data_time=datetime.datetime.now()
    delta=timedelta(minutes=3)
    
    while (True):
        
        s=''
        c=0
        c=UART.inWaiting()
        data=[]
        general_time = datetime.datetime.now()
        #print(general_time)
        #print(data_time)
        if (general_time-delta)>data_time:
            GPIO.output(16, GPIO.HIGH)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.HIGH)
            
        
        
        if c:
            s=UART.read(c)
            #print(s)
            for i in range (0,len(s)):
                data.append(chr(s[i]))
            if (len(data)==52):
                start=data[0]
                stop1=data[50]
                stop2=data[51]
                if (start is chr(START) and stop1 is chr(STOP1) and stop2 is chr(STOP2)):
                    #print ("Odebrano ramke")
                    data_time = datetime.datetime.now()
                    #print (data[4])
                    #ozone_data=data[1]+data[2]+data[3]+data[4]
                    ozone_data=data[10]+data[11]+data[12]+data[13]
                    if (is_ozone):
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
                        
                        error_ozone_sensor_data=data[44]
                        try:
                            error_ozone_sensor = int(error_ozone_sensor_data)
                        except ValueError:
                            error_ozone_sensor=None
                        
                    else:
                        ozone=None
                        ozone_temperature=None
                        ozone_humidity=None
                        error_ozone_sensor=None
                    if (is_no2):
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
                        error_no2_sensor_data=data[43]
                        try:
                            error_no2_sensor = int(error_no2_sensor_data)
                        except ValueError:
                            error_no2_sensor=None
                    else:
                        no2=None
                        no2_temperature=None
                        no2_humidity=None
                        error_no2_sensor=None
                    
                    if(is_co2):
                        co2_data=data[19]+data[20]+data[21]+data[22]
                        try:
                            co2 = int(co2_data)
                        except ValueError:
                            co2=None
                    else:
                        co2=None
                    
                    if(is_pm25):
                        pm25_data=data[23]+data[24]+data[25]+data[26]
                        try:
                            pm25 = int(pm25_data)
                        except ValueError:
                            pm25=None
                    else:
                        pm25=None
                    
                    if(is_pm10):
                        pm10_data=data[27]+data[28]+data[29]+data[30]
                        try:
                            pm10 = int(pm10_data)
                        except ValueError:
                            pm10=None
                    else:
                        pm10=None
                    
                    if(is_temp):
                        temp_data=data[31]+data[32]+data[33]+'.'+data[34]
                        try:
                            temp = float(temp_data)
                        except ValueError:
                            temp=None
                    else:
                        temp=None
                    
                    if(is_wind):
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
                    else:
                        wind_d=None
                        wind_s=None
                        wind_g=None
                    
                    error_vent_data=data[42]
                    try:
                        error_vent = int(error_vent_data)
                    except ValueError:
                        error_vent=None
                        
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
                        
                    #print("insert")
                    
                    air_quality = ovr_air_quality(ozone,no2,co2,pm25,pm10)
                    
                    insert_live(ozone,no2,co2,pm25,pm10,temp,wind_d,wind_s,wind_g,ozone_temperature,ozone_humidity,no2_temperature,no2_humidity,air_quality)
                    update_technical(error_vent,error_ozone_sensor,error_no2_sensor,heater,reserve)
                    delete_old()
                        #diode_color(ozone,no2,co2,pm25,pm10)
                        
        time.sleep(5)
        #print("tic")

time.sleep(30)
print("start")
    
connection= network_connection()

print(connection)
if (connection):
    measure()
else:
    print("No network")
    

    

