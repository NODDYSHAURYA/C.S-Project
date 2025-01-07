import streamlit as st
import requests
import matplotlib.pyplot as plt
import numpy as np

# Set page layout and title
st.set_page_config(page_title="Enhanced Eco-Friendly Gadget Dashboard", layout="wide")
st.title("Enhanced Eco-Friendly Gadget Dashboard")

# API Keys
OPENWEATHER_API_KEY = "4501aee27954f15fd53811ba2d48e8be"  # Your OpenWeather API key
NEWS_API_KEY = "3e7e57b970a146ad9f0fbb43100b1b72"  # Replace with your News API key
UNSPLASH_ACCESS_KEY = "M7thmktfAAslxTtuGRo0-vL1wp79LRZDL-wKOomCM5I"  # Replace with Unsplash API key

# City Selection with Scrollbar (Indian Cities)
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

# Fetch Pollution Data
def fetch_real_time_data(city):
    base_url = "http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    lat = indian_cities[city]["lat"]
    lon = indian_cities[city]["lon"]
    response = requests.get(base_url.format(lat=lat, lon=lon, api_key=OPENWEATHER_API_KEY))

    if response.status_code == 200:
        data = response.json()
        components = data["list"][0]["components"]
        aqi = data["list"][0]["main"]["aqi"]
        return {
            "PM2.5": components["pm2_5"],
            "PM10": components["pm10"],
            "CO": components["co"],
            "NOx": components["no2"],
            "AQI": aqi,
        }
    else:
        st.error("Error fetching pollution data")
        return None

# Fetch Real-Time News
def fetch_news(city):
    news_url = f"https://newsapi.org/v2/everything?q={city}+pollution&apiKey={NEWS_API_KEY}"
    response = requests.get(news_url)

    if response.status_code == 200:
        articles = response.json().get("articles", [])[:5]
        return [{"title": article["title"], "url": article["url"]} for article in articles]
    else:
        st.error("Error fetching news")
        return []

# Fetch Images
def fetch_images(city):
    unsplash_url = f"https://api.unsplash.com/search/photos?query={city}+pollution&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(unsplash_url)

    if response.status_code == 200:
        photos = response.json().get("results", [])[:5]
        return [photo["urls"]["small"] for photo in photos]
    else:
        st.error("Error fetching images")
        return []

# AQI Calculation
def calculate_aqi(pm25, pm10, co, nox):
    aqi = (pm25 + pm10 + co + nox) / 4
    return max(min(aqi, 500), 0)

# Plot AQI
def plot_aqi(aqi, title="Air Quality Index", color="skyblue"):
    fig, ax = plt.subplots()
    ax.barh(["AQI"], [aqi], color=color)
    ax.set_xlim(0, 500)
    ax.set_title(title)
    st.pyplot(fig)

# Plot Pollution Factors
def plot_pollution_factors(pm25, pm10, co, nox):
    factors = {"PM2.5": pm25, "PM10": pm10, "CO": co, "NOx": nox}
    labels, values = zip(*factors.items())
    fig, ax = plt.subplots()
    ax.barh(labels, values, color="lightgreen")
    ax.set_title("Pollution Factors")
    ax.set_xlabel("Concentration")
    st.pyplot(fig)

# Pollution Data and Visualization
pollution_data = fetch_real_time_data(selected_city)
if pollution_data:
    st.write(f"### Real-time Pollution Data for {selected_city}")
    st.write(pollution_data)
    plot_aqi(pollution_data["AQI"])
    plot_pollution_factors(
        pollution_data["PM2.5"], pollution_data["PM10"], pollution_data["CO"], pollution_data["NOx"]
    )

# User-Adjusted Pollution Factors
pm25_slider = st.sidebar.slider("PM2.5 (µg/m³)", 0, 500, pollution_data["PM2.5"] if pollution_data else 50)
pm10_slider = st.sidebar.slider("PM10 (µg/m³)", 0, 500, pollution_data["PM10"] if pollution_data else 50)
co_slider = st.sidebar.slider("CO (ppm)", 0, 2000, pollution_data["CO"] if pollution_data else 1)
nox_slider = st.sidebar.slider("NOx (ppb)", 0, 500, pollution_data["NOx"] if pollution_data else 50)

adjusted_aqi = calculate_aqi(pm25_slider, pm10_slider, co_slider, nox_slider)
st.write(f"### Adjusted AQI: {adjusted_aqi}")
plot_aqi(adjusted_aqi, title="Adjusted Air Quality Index", color="lightgreen")

# Display Real-Time News
news_articles = fetch_news(selected_city)
if news_articles:
    st.write(f"### Latest News on Pollution in {selected_city}")
    for article in news_articles:
        st.markdown(f"- [{article['title']}]({article['url']})")

# Display Images
images = fetch_images(selected_city)
if images:
    st.write(f"### Images Related to Pollution in {selected_city}")
    for img_url in images:
        st.image(img_url, use_column_width=True)

# User Instructions
st.sidebar.title("Instructions")
st.sidebar.info(
    "1. Select a city from the dropdown menu.\n"
    "2. View real-time pollution data, news, and images.\n"
    "3. Adjust pollution levels using sliders and see updated AQI."
)

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Developed by Shaurya Harish Dhupar")
