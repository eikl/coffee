import csv
import time
from sensirion_i2c_driver import I2cConnection, LinuxI2cTransceiver
from sensirion_i2c_sen5x import Sen5xI2cDevice
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
import datetime as dt
from luma.oled.device import sh1106
import matplotlib.pyplot as plt
from PIL import Image
#import pandas as pd
plt.rc('font', weight='bold')
with LinuxI2cTransceiver('/dev/i2c-1') as i2c_transceiver, open('/home/pi/oh_aq/measurements.csv', 'a', newline='') as file:
    device = Sen5xI2cDevice(I2cConnection(i2c_transceiver))
    serial = i2c(port=1, address=0x3C)
    screen=sh1106(serial)

    # Perform a device reset (reboot firmware)
    device.device_reset()

    # Start measurement
    device.start_measurement()

    writer = csv.writer(file)
    # Writing header to the CSV file
    pmlist = []
    timelist = []
    writer.writerow(["Time", "PM2.5", "Temperature", "Relative Humidity", "voc", "nox"])
    while True:
        # Wait until next result is available
        print("Waiting for new data...")
        while device.read_data_ready() is False:
            time.sleep(0.1)

        # Read measured values -> clears the "data ready" flag
        values = device.read_measured_values()
        print(values)
        # Access a specific value separately (see Sen5xMeasuredValues)
        mass_concentration = values.mass_concentration_2p5.physical
        pm10 = values.mass_concentration_10p0.physical
        ambient_temperature = values.ambient_temperature.degrees_celsius
        ambient_rh = values.ambient_humidity.percent_rh
        voc = values.voc_index.scaled
        nox = values.nox_index
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), mass_concentration, ambient_temperature, ambient_rh,voc,nox])
        print(len(timelist))
        if True:
            with canvas(screen) as draw:
                draw.rectangle(screen.bounding_box, outline='white', fill='black')
                draw.text((0,30), f'PM2.5: {mass_concentration}, PM10: {pm10}',fill='white')
                draw.text((0,50), f'VOC: {voc}, NOx: {nox}',fill='white')
                draw.text((0,40), f'T: {ambient_temperature}, RH: {ambient_rh}',fill='white')
        status = device.read_device_status()
        print("Device Status: {}\n".format(status))
        file.flush()