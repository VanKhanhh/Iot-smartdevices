import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib
import matplotlib.pyplot as plt

CSV_PATH = 'moisture_data.csv'      

# Read the timestamp and value columns
df = pd.read_csv(CSV_PATH, usecols=['created_at', 'value'])

df['created_at'] = pd.to_datetime(df['created_at'])
df['value'] = pd.to_numeric(df['value'], errors='coerce')
df.dropna(inplace=True)

df.sort_values('created_at', inplace=True)
df.reset_index(drop=True, inplace=True)

N_LAGS = 3           
for i in range(1, N_LAGS + 1):
    df[f'lag_{i}'] = df['value'].shift(i)

df.dropna(inplace=True)

X = df[[f'lag_{i}' for i in range(N_LAGS, 0, -1)]]
y = df['value']           

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)
print(f"R² on test set: {model.score(X_test, y_test):.3f}")

joblib.dump(model, 'moisture_predictor.pkl')
print(" Model saved as moisture_predictor.pkl")

latest_values = df['value'].tail(N_LAGS).values[::-1]  # [lag3, lag2, lag1]
predicted_next = model.predict([latest_values])[0]
print(f"Last {N_LAGS} readings: {latest_values}  ->  Predicted next: {predicted_next:.2f}")

# Visualization
plt.figure(figsize=(10,4))
plt.plot(df['created_at'], df['value'], label='Soil moisture (%)')
plt.xlabel('Time'); plt.ylabel('Moisture value')
plt.title('Soil Moisture Time‑series')
plt.grid(); plt.legend(); plt.tight_layout()
plt.show()
