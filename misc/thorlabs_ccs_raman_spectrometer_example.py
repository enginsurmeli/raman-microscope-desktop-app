# -*- coding: utf-8 -*-
"""
Example of C Libraries for CCS Spectrometers in Python with CTypes

"""
import os
import time
import matplotlib.pyplot as plt
from ctypes import *
import numpy as np

lib_folder = 'thorlabs_lib'
dll_filepath = os.path.join(os.path.dirname(
    __file__), '..', lib_folder, 'TLCCS_64.dll')
lib = cdll.LoadLibrary(dll_filepath)

# documentation: C:\Program Files\IVI Foundation\VISA\Win64\TLCCS\Manual

# Start Scan- Resource name will need to be adjusted
# windows device manager -> NI-VISA USB Device -> Spectrometer -> Properties -> Details -> Device Instance ID
# The resource name has this format: USB0::0x1313::<product ID>::<serial number>::RAW
#
# Product IDs are:
# 0x8081   // CCS100 Compact Spectrometer
# 0x8083   // CCS125 Special Spectrometer
# 0x8085   // CCS150 UV Spectrometer
# 0x8087   // CCS175 NIR Spectrometer
# 0x8089   // CCS200 UV-NIR Spectrometer
#
# The serial number is printed on the CCS spectrometer.
#
# E.g.: "USB0::0x1313::0x8081::M00822009::RAW" for a CCS100 with serial number M00822009

ccs_handle = c_int(0)
serial_number = "M00822009"
product_id = "0x8081"
device_address = bytes(f"USB0::0x1313::{product_id}::{serial_number}::RAW", 'utf-8')
connect_spectrometer = lib.tlccs_init(device_address, 1, 1, byref(ccs_handle))

if connect_spectrometer == 0:
    is_connected = True
    print("Spectrometer connected")
else:
    is_connected = False
    print("Spectrometer not connected")

if is_connected:

    # set integration time in  seconds, ranging from 1e-5 to 6e1
    integration_time = c_double(10)
    lib.tlccs_setIntegrationTime(ccs_handle, integration_time)

    # start scan
    lib.tlccs_startScan(ccs_handle)

    wavelengths = (c_double*3648)()

    lib.tlccs_getWavelengthData(ccs_handle, 0, byref(
        wavelengths), c_void_p(None), c_void_p(None))

    # retrieve data
    data_array = (c_double*3648)()
    lib.tlccs_getScanData(ccs_handle, byref(data_array))

    raman_shift_nm = np.ndarray(shape=(3648,), dtype=float, buffer=wavelengths)
    raman_shift_inverse_cm = 1e7*(1/532 - 1/raman_shift_nm)
    intensity = np.ndarray(shape=(3648,), dtype=float, buffer=data_array)

    # plot data
    plt.plot(raman_shift_inverse_cm, intensity)
    plt.xlabel("Wavelength [cm$^{-1}$]")
    plt.ylabel("Intensity [a.u.]")
    plt.grid(True)
    plt.show()

    # close
    lib.tlccs_close(ccs_handle)
