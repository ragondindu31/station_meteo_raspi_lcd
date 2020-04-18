CREATE DATABASE meteo_today;

CREATE USER 'meteo_today'@'%' IDENTIFIED BY 'meteo_today';

GRANT ALL PRIVILEGES ON meteo_today.* TO 'meteo_today'@'%';

FLUSH PRIVILEGES;

CREATE TABLE meteo_today.openweathermap_today (

  date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,

  temperature decimal(3,1) DEFAULT NULL,

  pressure decimal(6,2) DEFAULT NULL,

  humidity decimal(3,0) DEFAULT NULL,

  icon char(3) DEFAULT NULL,
  
  wind decimal(6,2) DEFAULT NULL,

  PRIMARY KEY (date)

);

