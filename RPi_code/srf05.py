import RPi.GPIO as GPIO
import time
import datetime as dt
import numpy as np
import pymysql
 
#set GPIO Pins
GPIO_TRIGGER = 24
GPIO_ECHO = 25
 
#set GPIO direction (IN / OUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#connect to jeff bezos

db = super_secret.db
cursor = db.cursor()
cursor.execute('USE srf05_data')
def distance():
	# set Trigger to HIGH
	GPIO.output(GPIO_TRIGGER, True)
 
	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)
 
	StartTime = time.time()
	StopTime = time.time()
 
	# save StartTime
	while GPIO.input(GPIO_ECHO) == 0:
		StartTime = time.time()
 
	# save time of arrival
	while GPIO.input(GPIO_ECHO) == 1:
		StopTime = time.time()
 
	# time difference between start and arrival
	TimeElapsed = StopTime - StartTime
	# multiply with the sonic speed (34300 cm/s)
	# and divide by 2, because there and back
    # ignore the effect of hot air on the speed of sound
	distance = (TimeElapsed * 34300) / 2
 
	return distance
 
if __name__ == '__main__':
    with open('out.txt','w') as file:
        file.write('time,distance\n')
        try:
            while True:
                distances = []
                for i in range(5):
                    dist = distance()
                    distances.append(dist)
                    time.sleep(0.1)
                now = dt.datetime.now()
                current_date = now.strftime('%Y-%m-%d %H:%M:%S')
                avg_distance = np.average(distances)
                print(f"distance from sensor is {np.average(distances)}")
                #write the distance and time to aws database
                cursor.execute('''
                insert into level_data(date,level) values (%s,%s)
                ''',(current_date,avg_distance))
                db.commit()
	    # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()
            db.close()
            print('database connection closed')

