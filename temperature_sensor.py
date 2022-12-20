from random import randint
from typing import Tuple

def inside_values()-> Tuple[float, int]:
    """Function for reading values from sensor

    Returns:
        Tuple[float, int]: temperature in ˚C and
                            humidity in %
    """

    temperature = randint(200, 220) / 10
    humidity = randint(50, 60)

    return temperature, humidity


def outside_values()-> Tuple[float, int, float]:
    """Function for receving values from bluetooth from arduino

    Returns:
        Tuple[float, int, float]: temperature in ˚C,
                                    humidity in % and
                                    pressure in kPa
    """

    temperature = randint(-5, 5) / 10
    humidity = randint(70, 90)
    pressure = randint(100000, 102000)/1000

    return temperature, humidity, pressure