import urllib.request
import json
import mysql.connector
import datetime


global actual_date
now = datetime.datetime.now()

def insert_new_record(id_stat):
    actual_date=str(now.year)+"-"+str(now.month)+"-"+str(now.day)+" "+str(now.hour)+":00:00"
    #actual_date=str(now.year)+"-"+str(now.month)+"-"+str(now.day)+" 12:00:00"

    try:
        mydb = mysql.connector.connect(host="79.189.200.10",port="3400",user="meteo_zam",passwd="2&X(jX]l@R$0=]4",database="meteo_zam")
        mycursor=mydb.cursor()
        #print (database_live)
        sql = "INSERT INTO measure_gios (id_station,measure_date) VALUES (%s,%s)"
        val = (id_stat,actual_date)
        mycursor.execute(sql, val)
        mydb.commit()
        
        print(now)

        print(mycursor.rowcount, id_stat+" record inserted.")
    except mysql.connector.Error as e:
        print ("Error code:", e.errno)        # error number
        print ("SQLSTATE value:", e.sqlstate) # SQLSTATE value
        print ("Error message:", e.msg )      # error message
        print ("Error:", e)                # errno, sqlstate, msg values
        s = str(e)
        print ("Error:", s)                  # errno, sqlstate, msg values



mydb = mysql.connector.connect(host="79.189.200.10",port="3400",user="meteo_zam",passwd="2&X(jX]l@R$0=]4",database="meteo_zam")
mycursor=mydb.cursor()
mycursor.execute("SELECT id_gios,so2,no2,pm10,pm25,co,c6h6,o3 FROM sensors_gios")
myresult = mycursor.fetchall()
for id_sens in myresult:
    id_station=id_sens[0]
    insert_new_record(id_station)