#! /usr/bin/env python3

import configparser, time, datetime, mysql.connector

###### Définition des requêtes SQL

# Affichage de la température et humidité uniquement si moins de 15 min

sql_sensor      ='SELECT date,temperature,humidity,battery FROM sensor_data WHERE date > (NOW() - INTERVAL 15 MINUTE) order by date DESC LIMIT 1'

# Affichage de l'icône principale de prévision météo

sql_forecast    ='SELECT icon,date FROM meteo.openweathermap WHERE date >  "{DATE}" ORDER BY date ASC LIMIT 1'

# Prévision météo pour les jours suivants à 9h et 15h

sql_forecast_3d ='SELECT icon,date FROM meteo.openweathermap WHERE date > ("{DATE}" + INTERVAL 1 DAY) AND (date like "%15:00:00" OR date like "%09:00:00") ORDER BY date ASC LIMIT 6;'

###### Fonctions utilitaire

# fonction de création de tuple à partir du fichier de configuration

def parse_int_values(value_to_split):

    return (tuple(map(int,value_to_split.split(','))))

###### Lecture du fichier de configuration

settings = configparser.ConfigParser()

settings._interpolation = configparser.ExtendedInterpolation()

settings.read('/home/pi/meteo/meteo.ini')

###### Lecture des informations de configuration
# Répertoire des images
img_dir=settings.get('display', 'img_dir')

# Intervalle de rafraîchissement des informations
#pas forcement utile a voir
refresh_rate   = int(settings.get('display', 'refresh'))

seconds_since_last_refesh = refresh_rate

# Paramétrage MySQL

mysql_config={

  'user':       settings.get('mysql', 'user'),

  'password':   settings.get('mysql', 'password'),

  'database':   settings.get('mysql', 'database'),

  'host':       settings.get('mysql', 'location')

}# Connexion à MySQL

cnx = mysql.connector.connect(**mysql_config)

while True :
    ######## mise a jour des données a afficher :
    now = datetime.datetime.now()

    if(seconds_since_last_refesh >= refresh_rate) :

            forecast_3d_icons=[]

            forecast_icon=[]

            txt_temperature=[]

            txt_humidity=[]

            cursor = cnx.cursor()

            # Date du jour à minuit

            midnight_date=now.strftime('%Y-%m-%d 00:00:00');

            # prochaine prévision météo

            cursor.execute(sql_forecast.replace('{DATE}',now.strftime('%Y-%m-%d %H:%M:%S')))

            for (icon,date) in cursor:

                forecast_icon.append(icon)

            # prévision météo sur les 3 jours à venir

            cursor.execute(sql_forecast_3d.replace('{DATE}',midnight_date))

            for (icon_3d,date) in cursor:

                forecast_3d_icons.append(icon_3d)

            seconds_since_last_refesh=0

            cursor.close()

            cnx.commit()

    #pour debug :
    #print(txt_temperature)
    #print(txt_humidity+'/n')
    #print(midnight_date+'/n')
    #print(now.strftime('%Y-%m-%d %H:%M:%S'))
    #print(str(forecast_icon))



    seconds_since_last_refesh+=1

    time.sleep(1)

cnx.close()

