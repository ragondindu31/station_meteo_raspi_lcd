import configparser, time, datetime, mysql.connector

###### Définition des requêtes SQL

# recuperation de l'icône principale de prévision météo et des infos de météo du jour :
sql_today   ='SELECT icon,temperature, pressure, humidity,wind, date FROM meteo_today.openweathermap_today ORDER BY date DESC LIMIT 1'


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

    today_icon=[]

    txt_temperature="__._"

    txt_pressure="__"

    txt_humidity="__._"

    txt_wind="__"

    date="00-00-0000"
    cursor = cnx.cursor()

    

    # icon et données du jour

    cursor.execute(sql_today)

    for (icon,temperature, pressure, humidity,wind, date) in cursor:

        today_icon.append(icon)

        txt_temperature=temperature

        txt_pressure= pressure

        txt_humidity=humidity

        txt_wind=wind

        date = date

    # Date du jour à minuit

    midnight_date=date
        

    cursor.close()

    cnx.commit()

    cnx.close()

    return txt_temperature, today_icon, txt_pressure, txt_humidity, txt_wind, date, midnight_date

#pour debug :
txt_temperature,today_icon, txt_pressure, txt_humidity, txt_wind, date, midnight_date = today_data()
print(midnight_date)
print(date)
# print(txt_temperature)
# print(txt_humidity)
# print(datadumoment(now.strftime('%Y-%m-%d %H:%M:%S')))
# print(str(datadumoment(today_icon)))
# print(datadumoment(txt_pressure))
# print(datadumoment(txt_wind))




