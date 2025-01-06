import streamlit as st
import requests
import matplotlib.pyplot as plt
import numpy as np

# Set page layout and title
st.set_page_config(page_title="Eco-Friendly Gadget Dashboard", layout="wide")
st.title("Eco-Friendly Gadget Dashboard")

# 1. **City Selection with Scrollbar (Indian Cities)**
indian_cities = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
    "Pune": {"lat": 18.5204, "lon": 73.8567},
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
    "Lucknow": {"lat": 26.8467, "lon": 80.9462},
    "Surat": {"lat": 21.1702, "lon": 72.8311},
    "Jaipur": {"lat": 26.9124, "lon": 75.7873},
    "Chandigarh": {"lat": 30.7333, "lon": 76.7794},
    "Indore": {"lat": 22.7196, "lon": 75.8577},
    "Bhopal": {"lat": 23.2599, "lon": 77.4126},
    "Nagpur": {"lat": 21.1458, "lon": 79.0882},
    "Patna": {"lat": 25.5941, "lon": 85.1376},
    "Vadodara": {"lat": 22.3072, "lon": 73.1812},
    "Coimbatore": {"lat": 11.0168, "lon": 76.9558},
    "Visakhapatnam": {"lat": 17.6869, "lon": 83.2185},
    "Madurai": {"lat": 9.9193, "lon": 78.1193}
}

selected_city = st.selectbox("Select City", list(indian_cities.keys()))

# 2. **Real-time Pollution Data from OpenWeather (Updated)**
def fetch_real_time_data(city):
    api_key = "4501aee27954f15fd53811ba2d48e8be"  # Replace with your API key
    base_url = "http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

    city_coordinates = {
        "Delhi": {"lat": 28.6139, "lon": 77.2090},
        "Mumbai": {"lat": 19.0760, "lon": 72.8777},
        "Kolkata": {"lat": 22.5726, "lon": 88.3639},
        "Chennai": {"lat": 13.0827, "lon": 80.2707},
        "Bangalore": {"lat": 12.9716, "lon": 77.5946},
        "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
        "Pune": {"lat": 18.5204, "lon": 73.8567},
        "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
        "Lucknow": {"lat": 26.8467, "lon": 80.9462},
        "Surat": {"lat": 21.1702, "lon": 72.8311},
        "Jaipur": {"lat": 26.9124, "lon": 75.7873},
        "Chandigarh": {"lat": 30.7333, "lon": 76.7794},
        "Indore": {"lat": 22.7196, "lon": 75.8577},
        "Bhopal": {"lat": 23.2599, "lon": 77.4126},
        "Nagpur": {"lat": 21.1458, "lon": 79.0882},
        "Patna": {"lat": 25.5941, "lon": 85.1376},
        "Vadodara": {"lat": 22.3072, "lon": 73.1812},
        "Coimbatore": {"lat": 11.0168, "lon": 76.9558},
        "Visakhapatnam": {"lat": 17.6869, "lon": 83.2185},
        "Madurai": {"lat": 9.9193, "lon": 78.1193}
    }

    lat = city_coordinates[city]["lat"]
    lon = city_coordinates[city]["lon"]

    response = requests.get(base_url.format(lat=lat, lon=lon, api_key=api_key))

    if response.status_code == 200:
        data = response.json()
        components = data["list"][0]["components"]
        aqi = data["list"][0]["main"]["aqi"]
        return {
            "PM2.5": components["pm2_5"],
            "PM10": components["pm10"],
            "CO": components["co"],
            "NOx": components["no2"],
            "AQI": aqi
        }
    else:
        print("Error fetching data:", response.status_code)
        return None

# 3. **Pollution Data and Sliders**
def pollution_sliders():
    st.sidebar.title("Adjust Pollution Factors")
    pm25_slider = st.sidebar.slider("PM2.5", 0, 500, 50)
    pm10_slider = st.sidebar.slider("PM10", 0, 500, 50)
    co_slider = st.sidebar.slider("CO (ppm)", 0, 2000, 1)
    nox_slider = st.sidebar.slider("NOx (ppb)", 0, 500, 50)

    return pm25_slider, pm10_slider, co_slider, nox_slider

# 4. **AQI Calculation**
def calculate_aqi(pm25, pm10, co, nox):
    aqi = (pm25 + pm10 + co + nox) / 4  # Simplified AQI calculation
    aqi = max(min(aqi, 1000), 0)  # Ensure AQI is within the valid range
    return aqi

# 5. **Graphics: Plotting AQI**
def plot_aqi(aqi):
    fig, ax = plt.subplots(figsize=(4, 2))  # Thinner graph vertically
    ax.barh(["AQI"], [aqi], color="skyblue")
    ax.set_xlim(0, 1000)
    ax.set_xlabel("Air Quality Index (AQI)")
    ax.set_title("AQI Level")
    st.pyplot(fig)

# 6. **Pollution Factors Visualization**
def plot_pollution_factors(pm25, pm10, co, nox):
    factors = {"PM2.5": pm25, "PM10": pm10, "CO": co, "NOx": nox}
    labels, values = zip(*factors.items())

    fig, ax = plt.subplots(figsize=(4, 3))  # Thinner graph vertically
    ax.barh(labels, values, color="lightgreen")
    ax.set_xlabel("Concentration")
    ax.set_title("Pollution Factors")
    st.pyplot(fig)

# 7. **Pollution News**
def get_pollution_news_for_city(city):
    news = {
        "Delhi": [
            {"headline": "Delhi's air quality deteriorates to hazardous levels.", "url": "https://www.google.com/search?q=Delhi+air+pollution"},
            {"headline": "Government announces stricter measures to combat air pollution in Delhi.", "url": "https://www.google.com/search?q=Delhi+pollution+measures"}
        ],
        "Mumbai": [
            {"headline": "Mumbai's air pollution rises due to increased vehicular emissions.", "url": "https://www.google.com/search?q=Mumbai+air+pollution+vehicular+emissions"},
            {"headline": "Experts warn of smog-related risks in Mumbai.", "url": "https://www.google.com/search?q=Mumbai+smog+health+risk"}
        ],
        "Kolkata": [
            {"headline": "Kolkata faces rising pollution levels from industrial emissions.", "url": "https://www.google.com/search?q=Kolkata+industrial+pollution"},
            {"headline": "Kolkata's air quality worsens, posing health risks.", "url": "https://www.google.com/search?q=Kolkata+air+quality+worsens"}
        ],
        "Chennai": [
            {"headline": "Chennai faces declining air quality due to high vehicular emissions.", "url": "https://www.google.com/search?q=Chennai+vehicular+emissions"},
            {"headline": "Experts caution about the growing pollution levels in Chennai.", "url": "https://www.google.com/search?q=Chennai+pollution+levels"}
        ],
        "Bangalore": [
            {"headline": "Bangalore's air quality drops due to construction and industrial emissions.", "url": "https://www.google.com/search?q=Bangalore+construction+pollution"},
            {"headline": "Bangalore government plans to regulate vehicular emissions.", "url": "https://www.google.com/search?q=Bangalore+vehicular+pollution+regulation"}
        ],
        "Hyderabad": [
            {"headline": "Hyderabad's air quality worsens due to increasing industrialization.", "url": "https://www.google.com/search?q=Hyderabad+industrial+pollution"},
            {"headline": "Experts call for urgent measures to reduce pollution in Hyderabad.", "url": "https://www.google.com/search?q=Hyderabad+pollution+measures"}
        ],
        "Pune": [
            {"headline": "Pune faces pollution crisis as vehicular emissions rise.", "url": "https://www.google.com/search?q=Pune+vehicular+emissions"},
            {"headline": "Pune government plans to cut pollution through green zones.", "url": "https://www.google.com/search?q=Pune+green+zones+pollution"}
        ],
        "Ahmedabad": [
            {"headline": "Ahmedabad sees rise in pollution levels due to industrial waste.", "url": "https://www.google.com/search?q=Ahmedabad+industrial+waste+pollution"},
            {"headline": "Ahmedabad residents seek better air quality measures.", "url": "https://www.google.com/search?q=Ahmedabad+residents+air+quality"}
        ],
        "Lucknow": [
            {"headline": "Lucknow's air quality drops due to high vehicular emissions.", "url": "https://www.google.com/search?q=Lucknow+vehicular+emissions"},
            {"headline": "Lucknow government works on solutions to curb pollution.", "url": "https://www.google.com/search?q=Lucknow+pollution+solutions"}
        ],
        "Surat": [
            {"headline": "Surat's pollution levels rise with industrial activities.", "url": "https://www.google.com/search?q=Surat+industrial+pollution"},
            {"headline": "Surat works on air quality improvements with better waste management.", "url": "https://www.google.com/search?q=Surat+air+quality+improvements"}
        ]
    }
    return news.get(city, [])

# 8. **Displaying the Data**
pollution_data = fetch_real_time_data(selected_city)
pm25, pm10, co, nox = pollution_data["PM2.5"], pollution_data["PM10"], pollution_data["CO"], pollution_data["NOx"]
city_aqi = calculate_aqi(pm25, pm10, co, nox)

# Show real-time pollution factors
st.write(f"Real-time Pollution Factors for {selected_city}:")
st.write(f"PM2.5: {pm25} µg/m³")
st.write(f"PM10: {pm10} µg/m³")
st.write(f"CO: {co} ppm")
st.write(f"NOx: {nox} µg/m³")

# Plot AQI
plot_aqi(city_aqi)

# Plot pollution factors
plot_pollution_factors(pm25, pm10, co, nox)

# Show pollution news
pollution_news = get_pollution_news_for_city(selected_city)
st.write(f"Latest Pollution News for {selected_city}:")
for article in pollution_news:
    st.markdown(f"- [{article['headline']}]({article['url']})")

# Allow users to adjust pollution levels via sliders
pm25_slider, pm10_slider, co_slider, nox_slider = pollution_sliders()

# Show updated AQI based on sliders
adjusted_aqi = calculate_aqi(pm25_slider, pm10_slider, co_slider, nox_slider)
st.write(f"Adjusted AQI (based on sliders): {adjusted_aqi}")

# Plot the adjusted AQI
plot_aqi(adjusted_aqi)
