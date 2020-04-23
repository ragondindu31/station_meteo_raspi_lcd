import configparser, time, datetime, mysql.connector

###### Définition des requêtes SQL

# recuperation de l'icône principale de prévision météo et des infos de météo du jour :

                                    #"""attention au format de demande d'infos :ORDER BY"""
sql_today   ='SELECT icon,temperature, pressure, humidity,wind, date FROM meteo_today.openweathermap_today ORDER BY date DESC LIMIT 1'

# recuperation des infos de previsions météo

sql_forecast ='SELECT icon,temperature,date FROM meteo.openweathermap WHERE date > ("{DATE}" + INTERVAL 1 DAY) AND (date like "%15:00:00" OR date like "%09:00:00") ORDER BY date ASC LIMIT 6;'

###### Lecture du fichier de configuration

settings = configparser.ConfigParser()

settings._interpolation = configparser.ExtendedInterpolation()

settings.read('/home/pi/meteo/meteo.ini')

###### Lecture des informations de configuration
# Répertoire des images
img_dir=settings.get('display', 'img_dir')

# Intervalle de rafraîchissement des informations
#pas forcement utile a voir
# refresh_rate   = int(settings.get('display', 'refresh'))

# seconds_since_last_refesh = refresh_rate
# seconds_since_last_refesh+=1
# seconds_since_last_refesh=0
# time.sleep(1)
######## mise a jour des données a afficher :
#    now = datetime.datetime.now()
####Actualisation des données du jour

def today_data():
# Paramétrage MySQL

    mysql_today_config={

    'user':       settings.get('mysql_today', 'user'),

    'password':   settings.get('mysql_today', 'password'),

    'database':   settings.get('mysql_today', 'database'),

    'host':       settings.get('mysql_today', 'location')  
    }
    # Connexion à MySQL_today
    cnx = mysql.connector.connect(**mysql_today_config)

    cursor = cnx.cursor()

    # icon et données du jour

    cursor.execute(sql_today)

    for (icon,temperature, pressure, humidity, wind, date) in cursor:

        dict_data_today = {}
    
        dict_data_today["today_icon"] = icon

        dict_data_today["temperature"] = temperature

        dict_data_today["pressure"] = int(pressure)

        dict_data_today["humidity"] = humidity

        dict_data_today["wind"]= wind

        dict_data_today["date"]= date

    cursor.close()

    cnx.commit()

    cnx.close()

    
    
    return dict_data_today

def data_forecast() :

    now = datetime.datetime.now()
    midnight_date=now.strftime('%Y-%m-%d 00:00:00');

    # Paramétrage MySQL
    mysql_forecast_config={

    'user':       settings.get('mysql_forecast', 'user'),

    'password':   settings.get('mysql_forecast', 'password'),

    'database':   settings.get('mysql_forecast', 'database'),

    'host':       settings.get('mysql_forecast', 'location')
    }

    # Connexion à MySQL
    cnx = mysql.connector.connect(**mysql_forecast_config)    

    forecast_icon=[]

    cursor = cnx.cursor()

    # prévision météo sur les 3 jours à venir
    
    cursor.execute(sql_forecast.replace('{DATE}',midnight_date))

    for (icon,temperature,date) in cursor:
        forecast_icon.append(date.strftime('%Y-%m-%d %H:%M:%S'))
        forecast_icon.append(icon)
        forecast_icon.append(float(temperature))

        

    cursor.close()

    cnx.commit()

    cnx.close()

    return forecast_icon





#pour debug :
#print fonction today_data

dict_data_today ={}
dict_data_today = today_data()
for cle,valeur in dict_data_today.items():
    print (cle, str(valeur))


#print fonction data_forecast

forecast_data=[]
forecast_data = data_forecast()
print (str(forecast_data))




