import RPi.GPIO as GPIO
import time
import datetime as dt
import numpy as np
import pymysql
import super_secret 
import VL53L0X

#connect to jeff bezos

db = super_secret.db
cursor = db.cursor()
cursor.execute('USE srf05_data')

#create a laser tof sensor object
tof = VL53L0X.VL53L0X()
def distance():
    tof.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)
    timing = tof.get_timing()
    if (timing<20000):
        timing = 20000
    print(f'timing {timing} ms')
    for count in range(100):
        distance = tof.get_distance()
        if distance > 0:
            print(f'distance from sensor is {distance}')
            return (distance/10)*-1.182135711619752+17.904981518515626
        time.sleep(timing/1000000)
    tof.stop_ranging()
 
if __name__ == '__main__':
    with open('out.txt','w') as file:
        file.write('time,distance\n')
        try:
            while True:
<<<<<<< Updated upstream
                distances = []
                for i in range(5):
                    dist = distance()
                    distances.append(dist)
                    time.sleep(0.1)
=======
>>>>>>> Stashed changes
                now = dt.datetime.now()
                dist = distance()
                current_date = now.strftime('%Y-%m-%d %H:%M:%S')
                #write the distance and time to aws database
                cursor.execute('''
                insert into level_data(date,level) values (%s,%s)
                ''',(current_date,dist))
                db.commit()
                print(f'distance from sensor is {distance}')
        # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()
            db.close()
            print('database connection closed')

