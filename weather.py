#! /usr/bin/env python3
# -*-coding:utf-8 -*
import configparser, json, datetime

import urllib.request

import mysql.connector

      

# Lecture du fichier de configuration

settings = configparser.ConfigParser()

settings._interpolation = configparser.ExtendedInterpolation()

settings.read('/home/pi/meteo/meteo.ini')

# Construction de l'url OpenWeatherMap

url_openweathermap  = settings.get('openweathermap', 'url') + '?id='    + settings.get('openweathermap', 'id') + '&units=' + settings.get('openweathermap', 'units') + '&APPID=' + settings.get('openweathermap', 'APPID')

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

cnx = mysql.connector.connect(user=settings.get('mysql', 'user'),

database=settings.get('mysql', 'database'),

password=settings.get('mysql', 'password'),

host=settings.get('mysql', 'location'))

cursor = cnx.cursor()

# Pour chaque prévision météo, on écrit ou remplace l'information en base

for item in infos["list"]:  

    date=item["dt_txt"]                

    icon=item["weather"][0]["icon"]

    temperature=item["main"]["temp"]

    humidity=item["main"]["humidity"] 

    pressure=item["main"]["pressure"]  

    cursor.execute('REPLACE INTO openweathermap VALUES (%s,%s,%s,%s,%s);',

    (date,str(temperature),str(pressure),str(humidity),icon))

    

# validation et fermeture de la connexion à la base de données

cnx.commit()

cursor.close()

cnx.close()