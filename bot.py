import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("8630478159:AAHjpuWY-NZZ7mTKWK3kLgE8NQokd3dm32Y")
WEATHER_API_KEY = os.getenv("ab9d6b2c0de6ada464d3be8af4f367f1")
# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text()
    "👋 Send me a city name and I'll give you real-time weather 🌦️ and local time 🕒"
# Handle messages
async def get_weather_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text.strip()
    if not city:
        await update.message.reply_text("❌ Please send a city name.")
        return
    # Use OpenWeatherMap to fetch weather and timezone
    try:
        weather_response = requests.get(
            "http://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city,
                "appid": ("ab9d6b2c0de6ada464d3be8af4f367f1"),
                "units": "metric"
            },
            timeout=10
        ).json()
    except requests.RequestException:
        await update.message.reply_text("⚠️ Could not connect to the weather service.")
        return
    # If we get a valid response, calculate local time
    try:
        temp = weather_response["main"]["temp"]
        description = weather_response["weather"][0]["description"].capitalize()
        timezone_offset = weather_response["timezone"]  # seconds

        utc_now = datetime.utcnow()
        city_time = utc_now + timedelta(seconds=timezone_offset)
        current_time_str = city_time.strftime("%Y-%m-%d %H:%M:%S")

        city_name = weather_response.get("name", city)
        reply = (
            f"📍 City: {city_name}\n"
            f"🌡 Temperature: {temp}°C\n"
            f"🌥 Condition: {description}\n"
            f"🕒 Local Time: {current_time_str}"
        )
        await update.message.reply_text(reply)
    except Exception:
        await update.message.reply_text("⚠️ Could not fetch data for this city.")

# Main function
def main():
    app = ApplicationBuilder().token("8630478159:AAHjpuWY-NZZ7mTKWK3kLgE8NQokd3dm32Y").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather_time))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

    print("🤖 Bot is running...")