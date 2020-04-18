#! /usr/bin/env python3

import configparser, json, datetime

import urllib.request

import mysql.connector

from datetime import datetime 
      

# Lecture du fichier de configuration

settings = configparser.ConfigParser()

settings._interpolation = configparser.ExtendedInterpolation()

settings.read('/home/pi/meteo/meteo.ini')

# Construction de l'url OpenWeatherMap_today

url_openweathermap  = settings.get('openweathermap_today', 'url') + '?id='    + settings.get('openweathermap_today', 'id') + '&units=' + settings.get('openweathermap_today', 'units') + '&APPID=' + settings.get('openweathermap_today', 'APPID')

try:

    # Récupération des prévisions météo et décodage JSON

    webURL = urllib.request.urlopen(url_openweathermap)

    data = webURL.read()

    encoding = webURL.info().get_content_charset('utf-8')

    infos=json.loads(data.decode(encoding))

except:

    print("error reading url: "+url_openweathermap);

    exit(1)

# Connexion à la base de données à l'aide des paramètres de configuration

cnx = mysql.connector.connect(user=settings.get('mysql_today', 'user'),

database=settings.get('mysql_today', 'database'),

password=settings.get('mysql_today', 'password'),

host=settings.get('mysql_today', 'location'))

cursor = cnx.cursor()

# Pour chaque prévision météo, on écrit ou remplace l'information en base
for item in infos:
    for item in infos["weather"]:  

        icon=item["icon"]
        print()
    date=datetime.fromtimestamp(infos["dt"])
    print(date)
    temperature=infos["main"]["temp"]
    print(temperature)
    humidity=infos["main"]["humidity"] 
    print(humidity)
    pressure=infos["main"]["pressure"]  
    print(pressure)
    wind=infos["wind"]["speed"]  
    print(wind)
    cursor.execute('REPLACE INTO openweathermap_today VALUES (%s,%s,%s,%s,%s,%s);',

    (date,str(temperature),str(pressure),str(humidity),icon,str(wind)))

    

# validation et fermeture de la connexion à la base de données

cnx.commit()

cursor.close()

cnx.close()