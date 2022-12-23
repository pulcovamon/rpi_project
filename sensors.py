from random import randint
from typing import Tuple
import serial

def connection():
    """_summary_

    Returns:
        _type_: _description_
    """

    device = '/dev/HMSoft'
    baud_rate = 9600

    s = serial.Serial(device, baud_rate)

    return s


def inside_values()-> Tuple[float, int]:
    """Function for reading values from sensor

    Returns:
        Tuple[float, int]: temperature in ˚C and
                            humidity in %
    """

    temperature = randint(200, 220) / 10
    humidity = randint(50, 60)
    pressure = randint(100000, 102000)/1000

    return temperature, humidity, pressure


def outside_values(s)-> Tuple[float, int, float]:
    """Function for receving values from bluetooth from arduino

    Args:
        s: instance of bluetooth communication

    Returns:
        Tuple[float, int, float]: temperature in ˚C,
                                    humidity in % and
                                    pressure in kPa
    """

    temperature = s.read(0)
    humidity = s.read(1)

    return temperature, humidity