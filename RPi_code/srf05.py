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
try:
    db = super_secret.db
    cursor = db.cursor()
    cursor.execute('USE srf05_data')
except:
    print("Couldn't connect to database")
    quit()

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
    #
    # Take sample_length ammount of measurements. 
    # wait 1 second between measurements
    #
    samples = []
    for i in range(sample_length):
        samples.append(calibration(vl53.range))
    # return the average
    return np.average(samples)

 
if __name__ == '__main__':
    sample_number = 10
    with open('out.txt','w') as file:

        current_day = dt.datetime.now().weekday()

        viikonloppu = current_day >= 5
        
        file.write('time,distance\n')
        try:
            while not viikonloppu:
                #Get the time before the measuremnet starts

                now = dt.datetime.now()
                current_date = now.strftime('%Y-%m-%d %H:%M:%S')
                dist = distance(100)

                #write the distance and time to aws database
                try:
                    cursor.execute('''
                    insert into level_data(date,level) values (%s,%s)
                    ''',(current_date,dist))
                    db.commit()
                except:
                    print("Couldn't connect to database")
                print(f'distance from sensor is {dist}')

        # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            print("Measurement stopped by User")
            db.close()
            print('database connection closed')

