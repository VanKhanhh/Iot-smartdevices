from Adafruit_IO import MQTTClient
from counterfit_shims_grove.grove_relay import GroveRelay

# Adafruit IO credentials
ADAFRUIT_IO_USERNAME = ""                           # Replace with your Adafruit IO username
ADAFRUIT_IO_KEY = ""                                # Replace with your Adafruit IO Key

# Feed names
LIGHT_FEED = 'light'
TEMP_FEED = 'temp'
HUMID_FEED = 'humid'
RELAY_FEED = 'relay'

# Initialize relay
relay = GroveRelay(2)
relay_mqtt_state = "OFF"


# Command handler
def command_received(client, feed_id, payload):
    global relay_mqtt_state
    print(f"Command received: {feed_id} = {payload}")
    if feed_id == RELAY_FEED:
        relay_mqtt_state = payload.upper()

# Create and configure the client
aio_client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
aio_client.on_message = command_received
aio_client.connect()
aio_client.subscribe(RELAY_FEED)
aio_client.loop_background()
