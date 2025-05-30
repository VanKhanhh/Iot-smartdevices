import time 
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_seeed_python_dht import DHT
from counterfit_shims_grove.grove_relay import GroveRelay
from adafruit_io_client import aio_client, LIGHT_FEED, TEMP_FEED, HUMID_FEED, RELAY_FEED, relay_mqtt_state

CounterFitConnection.init('127.0.0.1', 5000)

dht_sensor = DHT("11", 5)
light_sensor = GroveLightSensor(0)
relay = GroveRelay(2)

while True:
    light = light_sensor.light
    print("Light level:", light)

    humid, temp = dht_sensor.read()
    print(f"Humidity: {humid}, Temperature: {temp}")

    # if relay_mqtt_state == "OFF":
    #     if humid < 80:
    #         print("Humidity low — Turn ON relay")
    #         relay.on()
    #         current_relay_state = "ON"
    #     else:
    #         print("Humidity OK")
    #         if relay_mqtt_state == "ON":
    #             relay.off()
    #             current_relay_state = "OFF"

    if humid < 80 :
        print("Soil moisture is low - Turn on the relay")
        relay.on()
        current_relay_state = "ON"
    else : 
        print("Soil moisture is OK - Turn off the relay")
        relay.off()
        current_relay_state = "OFF"


    aio_client.publish(LIGHT_FEED, light)
    aio_client.publish(TEMP_FEED, temp)
    aio_client.publish(HUMID_FEED, humid)
    aio_client.publish(RELAY_FEED, current_relay_state)

    time.sleep(5)
