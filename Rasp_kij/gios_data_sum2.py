import urllib.request
import json
import mysql.connector
import datetime

global id_data
id_data=[]
global now
global actual_date

def download_id_data():
    global id_data
    mydb = mysql.connector.connect(host="79.189.200.10",port="3400",user="meteo_zam",passwd="2&X(jX]l@R$0=]4",database="meteo_zam")
    mycursor=mydb.cursor()
    mycursor.execute("SELECT id_gios,so2,no2,pm10,pm25,co,c6h6,o3 FROM sensors_gios")
    id_data = mycursor.fetchall()
    #for id_sens in myresult:
     #   id_data_stat=id_sens
        #url_data_station="http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/"+str(id_station)

def update_station_data(station_id,station_date,station_value):

    try:
        mydb = mysql.connector.connect(host="79.189.200.10",port="3400",user="meteo_zam",passwd="2&X(jX]l@R$0=]4",database="meteo_zam")
        mycursor=mydb.cursor()
        #print (database_live)
        sql = "UPDATE measure_gios SET air_index = %s WHERE id_station = %s AND measure_date = %s"
        val = (station_value,station_id,station_date)
        mycursor.execute(sql, val)
        mydb.commit()

        print(mycursor.rowcount, station_id+" station at "+station_date+" updated.")
    except mysql.connector.Error as e:
        print ("Error code:", e.errno)        # error number
        print ("SQLSTATE value:", e.sqlstate) # SQLSTATE value
        print ("Error message:", e.msg )      # error message
        print ("Error:", e)                # errno, sqlstate, msg values
        s = str(e)
        print ("Error:", s)                  # errno, sqlstate, msg values


def download_station_data():
    for id_station in id_data:
        url_station_data="http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/"+str(id_station[0])
    
        with urllib.request.urlopen(url_station_data) as url_station:
            url_json_station = url_station.read()
            station_data = json.loads(url_json_station)
            
            #print(station_value_id)
            try:
                station_date = station_data["stSourceDataDate"]
                station_value = station_data["stIndexLevel"]
                station_value_id=station_value['id']
                #station_hour=station_date[11]+station_date[12]
                update_station_data(id_station[0],station_date,station_value_id)
                
            except:
                print("No data")

def download_sensor_data():
    for id_sensors in id_data:
        for id_sens in id_sensors:
            #pierwszy to id station
            if id_sens is not None:
                url_sensor_data="http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/"+str(id_sens)
                with urllib.request.urlopen(url_sensor_data) as url_sensor:
                    url_json_sensor = url_sensor.read()
                    station_data = json.loads(url_json_sensor)

now = datetime.datetime.now()
actual_hour=now.hour
actual_date=str(now.year)+"-"+str(now.month)+"-"+str(now.day)+" "+str(now.hour)+":00:00"

download_id_data()
download_station_data()
#download_sensor_data()

