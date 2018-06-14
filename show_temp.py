#!/usr/bin/python3
from scientificdevices.lakeshore.model340 import Model340


if __name__ == '__main__':
    temperature_device = Model340(address=12)

    temperature = temperature_device.get_temperature()

    print('Current temperature is: {:.2f} K'.format(temperature))

