# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the MAX31865 thermocouple amplifier.
# Will print the temperature every second.
import time
import board
import digitalio
import adafruit_max31865
import pymysql
import super_secret
import datetime as dt
#connect to jeff bezos
try:
   db = super_secret.db
   cursor = db.cursor()
   cursor.execute('USE srf05_data')
except:
   print("Couldn't connect to database")
   quit()

# Create sensor object, communicating over the board's default SPI bus
spi = board.SPI()
cs1 = digitalio.DigitalInOut(board.D22)  # Chip select of the MAX31865 board.
cs2 = digitalio.DigitalInOut(board.D27)
sensor1 = adafruit_max31865.MAX31865(spi, cs1)
sensor2 = adafruit_max31865.MAX31865(spi, cs2)
# Note you can optionally provide the thermocouple RTD nominal, the reference
# resistance, and the number of wires for the sensor (2 the default, 3, or 4)
# with keyword args:
# sensor = adafruit_max31865.MAX31865(spi, cs, rtd_nominal=100, ref_resistor=430.0, wires=2)

# Main loop to print the temperature every second.
while True:
    # Read temperature.
    temp1 = sensor1.temperature
    temp2 = sensor2.temperature
    print(temp1,temp2)
    current_date = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        cursor.execute("insert into level_data(date,temp_1,temp_2) values (%s,%s,%s)",(current_date,temp1,temp2))
        #cursor.execute('insert into level_data(date,temp_2) values (%s,%s)',(current_date,temp2))
        db.commit()
    except:
        print('could not connect to db')
    time.sleep(1)
