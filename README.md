

# Coffee level monitoring application

# Table of Contents


- [Coffee level monitoring application](#coffee-level-monitoring-application)
- [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Hardware](#hardware)
    - [Calibration procedure](#calibration-procedure)
        - [pic of plot and setup](#pic-of-plot-and-setup)
  - [Software](#software)
  - [Database structure](#database-structure)
  - [Todo](#todo)

## Introduction
Many students of Kumpula's physics building find themselves pondering the question: <br><br>
"_Is there coffee at OH right now?_"<br><br>
This project aims to answer that question by implementing IoT functionality into OH:s Moccamaster.
<br><br>
## Hardware
At the heart of this project is the Raspberry Pi computer equipped with the SRF-05 ultrasonic distance sensor. With this sensor we can effectively measure the amount of liquid (coffee) in the pan at any moment.
<br>
The distance sensor must be positioned in such a way that:
* It can always see the liquid surface
* The measured distance with no coffee pan in place is much larger than the distance which corresponds to an empty pan.
* It is not a nuisance to the average coffee enjoyer, and does not require special attention to produce proper readings

To achieve this, modifications may have to be made to the coffee machine.

### Calibration procedure
To calibrate the instrument, we compare the distance reading of the SRF-05 to some "precisely" measured volume of liquid. The relationship between the measured distance from the sensor and liquid level in the pan is not linear, and is probably easiest to find by interpolation. Testing is ongoing.
##### pic of plot and setup
<br>
Once we know this relationship, we can calculate the level of liquid from the measured distance. This is done by adding the fitting parameters to the function `insert_function_name()` in `srf05.py`.
<br><br>

## Software
The project consists of two main programs, `srf05.py` and `flask_app.py`. The former does the actual measurement and calculation of the coffee consumption. It then sends this data to our database. <br> The latter fetches this data from our database, and displays it in a web app.
<br><br>

## Database structure
The data produced by the RPi is stored in a MySQL database. The database has two tables, level_data and consumption_data:
| level_data      |               |
| --------------- |:-------------:|
| date (datetime) | level (float) | 

| consumption_data |
| ---------------- |
| volume (float)   |


## Todo 
* Mechanical design of parts to attach sensor and RPi to the Moccamaster
* Documentation of the calibration procedure
* Make the css/html code that makes the webpage nice to look at
* Figure out how to host the webpage with AWS
* Figure out how to get internet in OH