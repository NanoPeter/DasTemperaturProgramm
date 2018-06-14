#!/usr/bin/python3
from scientificdevices.lakeshore.model340 import Model340, RampStatus


if __name__ == '__main__':
    temperature_device = Model340(address=12)

    temperature = temperature_device.get_temperature()
    ramp_status = temperature_device.get_rampstatus()

    print('current temperature is: {:.2f} K ({})'.format(temperature), ramp_status.name)

