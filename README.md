

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
At the heart of this project is the Raspberry Pi computer equipped with the VL53L0X time-of-flight laser distance sensor. With this sensor we can effectively measure the amount of liquid (coffee) in the pan at any moment.
<br>
The distance sensor must be positioned in such a way that:
* It can always see the liquid surface
* The measured distance with no coffee pan in place is much larger than the distance which corresponds to an empty pan.
* It is not a nuisance to the average coffee enjoyer, and does not require special attention to produce proper readings

To achieve this, modifications may have to be made to the coffee machine.

### Calibration procedure
To calibrate the instrument, we compare the distance reading of the VL53L0X to some "precisely" measured volume of liquid. Once we have determined the relationship between the volume of coffee and the distance measured by the sensor (it should be quite close to linear), we can simply calculate the volume of coffee based on the distance.
##### pic of plot and setup
<br>

This is done by adding the fitting parameters to the function `insert_function_name()` in `srf05.py`.
<br><br>
## Software
The program is split into two folders, webpage_code and RPi_code.
#RPi_code
This folder contains code that is run on the Raspberry Pi.<br>
`srf05.py`
<br>
`distance()`
<br>
This function uses the included library for the VL53L0X sensor to determine the distance between the coffee and the sensor.
<br>
`calibration(distance)`
<br>
This function takes distance in millimeters as an input, and returns the level of coffee based on a calibration.
<br>
`main`
In the main loop the program writes the measurement time and result into a database.
<br>
### Required dependencies
The required dependencies are listed in `requirements.txt`, and can be installed with the command `pip install -r requirements.txt`. Note that `srf05.py` uses the `RPi.GPIO` library, which is preinstalled on most Raspberry Pi SBC:s
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
* Maybe implement a CO2 and TVOC (total volatile organic compound) sensor to create a sort of "pöhinäkerroin"
* Once this first prototype with RPi is working and calibrated, start thinking about the second version, and the possibility of a smaller microcontroller that is battery powered and embedded in the coffee pans handle
