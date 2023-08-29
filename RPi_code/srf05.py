import RPi.GPIO as GPIO
import time
import busio
import board
import adafruit_vl53l0x
import datetime as dt
import numpy as np
import pymysql
import super_secret 

#connect to jeff bezos

db = super_secret.db
cursor = db.cursor()
cursor.execute('USE srf05_data')

#
# Initialize i2c bus and sensor
#

i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

#
# Set timing for slower, but more accurate measurement
#

vl53.measurement_timing_budget = 200000

def calibration(distance):
    #
    # This function calculates the ammount of coffee in the pan
    # based on a calibration
    # The calibration procedure is described in README.md
    k = -1.182135711619752
    b = 17.904981518515626
    ammount_of_coffee = (distance/10)*k+b
    return ammount_of_coffee

def distance(sample_length):
    samples = []
    # take i measurements, 1 measurement is 1 second
    for i in range(sample_length):
        samples.append(vl53.range)
    # return the average
    return np.average(samples)

 
if __name__ == '__main__':
    #
    # Take 10 1 second samples
    #
    sample_number = 10
    with open('out.txt','w') as file:
        file.write('time,distance\n')
        try:
            while True:
                #Get the time before the measuremnet starts
                now = dt.datetime.now()
                current_date = now.strftime('%Y-%m-%d %H:%M:%S')
                dist = distance(sample_length=sample_number)
                #write the distance and time to aws database
                cursor.execute('''
                insert into level_data(date,level) values (%s,%s)
                ''',(current_date,dist))
                db.commit()
                print(f'distance from sensor is {distance}')
        # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            print("Measurement stopped by User")
            db.close()
            print('database connection closed')

