import urllib.request
import json
import mysql.connector
import datetime
now = datetime.datetime.now()


def insert_gios_data(id_sensor,date,value):
    try:
        mydb = mysql.connector.connect(host="79.189.200.10",port="3400",user="meteo_zam",passwd="2&X(jX]l@R$0=]4",database="meteo_zam")
        mycursor=mydb.cursor()
        #print (database_live)
        sql="INSERT INTO measure_gios (id_gsen,date,value) VALUES (%s,%s,%s)" 
        val= id_sensor,date,value                    
        mycursor.execute(sql,val)
        mydb.commit()
        
        now2 = datetime.datetime.now()
        print(now2)

        print(mycursor.rowcount, " new data inserted.")
    except mysql.connector.Error as e:
        print ("Error code:", e.errno)        # error number
        print ("SQLSTATE value:", e.sqlstate) # SQLSTATE value
        print ("Error message:", e.msg )      # error message
        print ("Error:", e)                # errno, sqlstate, msg values
        s = str(e)
        print ("Error:", s)                  # errno, sqlstate, msg values



actual_hour=now.hour
mydb = mysql.connector.connect(host="79.189.200.10",port="3400",user="meteo_zam",passwd="2&X(jX]l@R$0=]4",database="meteo_zam")
mycursor=mydb.cursor()
mycursor.execute("SELECT so2,no2,pm10,pm25,co,c6h6,o3 FROM sensors_gios")
myresult = mycursor.fetchall()
for id_sens in myresult:
    for x in range(7):
        sensor_id2 = id_sens[x]
        #print(sensor_id)
        if sensor_id2 is not None:
            sensor_id = int(sensor_id2)
            url_data = "http://api.gios.gov.pl/pjp-api/rest/data/getData/"+str(sensor_id)
            #print (url_data)
#     +str(sensor_id)
#url_sensors = "http://api.gios.gov.pl/pjp-api/rest/station/sensors/14"
#url_address="http://api.gios.gov.pl/pjp-api/rest/station/findAll"

            with urllib.request.urlopen(url_data) as url:
                url_db = url.read()
                sensor_data = json.loads(url_db)
    #print (sensor_data)
    #for sdat in sensor_data:
                sensor_param = sensor_data["key"]
                sensor_values = sensor_data["values"]
                try:
                    sensor_values2=sensor_values[0]
                    sensor_values_date=sensor_values2["date"]
                    sensor_hour=sensor_values_date[11]+sensor_values_date[12]
                    if actual_hour is int(sensor_hour):
                        sensor_values_value=sensor_values2["value"]
                        #sql_insert="INSERT INTO measure_gios (id_gsen,date,value) VALUES ("+sensor_id+","+sensor_hour+","+sensor_values_value+")" 
                        insert_gios_data(sensor_id,sensor_values_date,round(sensor_values_value))
                        #print("/////")
                        #print (str(sensor_param))
                        #print (str(sensor_values_date))
                        #print (round(sensor_values_value,0))
                except:
                    print ("No data")
