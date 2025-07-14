import serial
import time
from Adafruit_IO import Client
import joblib
import numpy as np
import pandas as pd

# Adafruit IO credentials
AIO_USERNAME = "vanphann"
AIO_KEY = ""
aio = Client(AIO_USERNAME, AIO_KEY)

# Connect to Arduino on COM4
ser = serial.Serial('COM4', 9600)

# Load trained ML model
try:
    model = joblib.load('moisture_predictor.pkl')
    print("ML model loaded.")
except Exception as e:
    model = None
    print("Cannot find ML model. Run manually:", e)

# Keep track of the last 3 moisture readings
history = []

while True:
    try:
        if ser.in_waiting:
            line = ser.readline().decode().strip()
            if not line.isdigit():
                continue  # Skip invalid lines

            moisture = int(line)
            print(f"Current soil moisture: {moisture}%")

            # Append to history for prediction
            history.append(moisture)
            if len(history) > 3:
                history.pop(0)

            # Send soil moisture value to Adafruit IO
            try:
                aio.send('soil-moisture', moisture)
            except Exception as e:
                print("Error sending soil moisture to Adafruit IO:", e)

            # Predict future moisture using ML model 
            if model and len(history) == 3:
                try:
                    if hasattr(model, 'feature_names_in_'):
                        feature_names = list(model.feature_names_in_)
                    else:
                        feature_names = ["lag_1", "lag_2", "lag_3"]
                    input_data = pd.DataFrame([history], columns=feature_names)
                    prediction = model.predict(input_data)
                    predicted_value = round(prediction[0], 2)
                    print(f"Predicted next soil moisture value: {predicted_value}%")
                    aio.send('predicted-moisture', predicted_value)
                except Exception as e:
                    print("Prediction error:", e)

            # Determine relay state
            relay_state = "ON" if moisture < 60 else "OFF"
            try:
                aio.send('relay', relay_state)
                print(f"Relay: {relay_state}")
            except Exception as e:
                print("Error sending relay state to Adafruit IO:", e)

        time.sleep(1200)  

    except KeyboardInterrupt:
        print("Program interrupted manually.")
        break
    except Exception as e:
        print("General error:", e)
        time.sleep(5)
