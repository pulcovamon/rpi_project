import bluetooth
import json
from influxdb import InfluxDBClient
import datetime


def connecting():
    sensor_address = '98:D3:61:FD:74:C3'
    socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    socket.connect((sensor_address, 1))

    influx = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')
    influx.create_database('example')

    def log_stats(client, sensor_address, stats):
        json_body = [
            {
                "measurement": "sensor_data",
                "tags": {
                    "client": sensor_address,
                },
                "time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "fields": {
                    "temperature": stats['temperature'],
                    "humidity": stats['humidity'],
                }
            }
        ]

        client.write_points(json_body)

    buffer = ""

    while True:
        data = socket.recv(1024)
        buffer += str(data, encoding='ascii')
        try:
            data = json.loads(buffer)
            print("Received chunk", data)
            log_stats(influx, sensor_address, data)
            buffer = ""
        except json.JSONDecodeError as e:
            continue

    socket.close()

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

if __name__ == '__main__':
    connecting()