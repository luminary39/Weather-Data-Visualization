import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# -----------------------
# Get weather data
# -----------------------

def get_weather_data(latitude, longitude):
    today = datetime.now() 
    week_ago = today - timedelta(days=7)
    start_date = week_ago.strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min"
    response = requests.get(url)
    data = response.json()
    return data

# ---------------------------------------------------------
# Setting-up Coordinates of 8 divisional cities in a Dict
# ---------------------------------------------------------

cities = {
    "Dhaka": (23.7289, 90.3944),
    "Chattogram": (22.3350, 91.8325),
    "Rajshahi": (24.3667, 88.6000),
    "Khulna": (22.8167, 89.5500),
    "Barishal": (22.70497, 90.370127),
    "Sylhet": (24.9000, 91.8667),
    "Rangpur": (25.6496, 89.2369),
    "Mymensingh": (24.6988, 90.4287)
}



# ------------------------------------------------
# gETTING WEATHER DATA IN A VARIABLE
# ------------------------------------------------

latitude, longitude= cities["Dhaka"]
data = get_weather_data(latitude=latitude, longitude=longitude)


# ------------------------------------------------
# process, visualize and save data in a file
# ------------------------------------------------


# 2. Process with pandas
df = pd.DataFrame({
    'date': pd.to_datetime(data['daily']['time']),
    'max_temp': data['daily']['temperature_2m_max'],
    'min_temp': data['daily']['temperature_2m_min']
})

# 3. Calculate average
df['avg_temp'] = (df['max_temp'] + df['min_temp']) / 2

# 4. Create visualization
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['max_temp'], 'r-o', label='Max')
plt.plot(df['date'], df['min_temp'], 'b-o', label='Min')
plt.plot(df['date'], df['avg_temp'], 'g--', label='Average')

plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title('Paris Weather - Past Week')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()

# 5. Save everything
os.makedirs("output", exist_ok=True)
plt.savefig("output/dhaka_chart.png")
df.to_csv("output/dhaka_weather.csv", index=False)

print(f"Average temperature: {df['avg_temp'].mean():.1f}°C")
print("Files saved in 'data' folder")

