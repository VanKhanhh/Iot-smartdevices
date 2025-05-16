import time 
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_seeed_python_dht import DHT
from counterfit_shims_grove.grove_relay import GroveRelay
from adafruit_io_client import aio_client, LIGHT_FEED, TEMP_FEED, HUMID_FEED, relay_mqtt_state


CounterFitConnection.init('127.0.0.1', 5000)

dht_sensor = DHT("11", 5)
light_sensor = GroveLightSensor(0)
relay = GroveRelay(2)


while True:
    light = light_sensor.light
    print("light level: ", light)

    humid, temp = dht_sensor.read()
    print(f"{humid}, {temp}")

    if relay_mqtt_state == "ON" or humid < 80 :
        print("Turn on relay")
        relay.on()
    else :
        relay.off()

    # Publish sensor data to Adafruit IO
    aio_client.publish(LIGHT_FEED, light)
    aio_client.publish(TEMP_FEED, temp)
    aio_client.publish(HUMID_FEED, humid)

    time.sleep(5)