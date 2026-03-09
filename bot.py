BOT_TOKEN=("8630478159:AAHjpuWY-NZZ7mTKWK3kLgE8NQokd3dm32Y")
WEATHER_API_KEY=("2435de8ab0de4109af56da0ba7e9352d")
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("8630478159:AAHjpuWY-NZZ7mTKWK3kLgE8NQokd3dm32Y")
WEATHER_API_KEY = os.getenv("2435de8ab0de4109af56da0ba7e9352d")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send /weather <city>\nExample: /weather London"
    )

# Weather command
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Please provide a city name.")
        return

    city = " ".join(context.args)

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={"2435de8ab0de4109af56da0ba7e9352d"}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            await update.message.reply_text("City not found.")
            return

        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        timezone_offset = data["timezone"]

        local_time = datetime.utcnow() + timedelta(seconds=timezone_offset)

        reply = (
            f"📍 City: {data['name']}\n"
            f"🌡 Temperature: {temperature}°C\n"
            f"🌤 Condition: {description}\n"
            f"⏰ Local Time: {local_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        await update.message.reply_text(reply)

    except Exception:
        await update.message.reply_text("Error fetching data.")

# Main function
if __name__ == "__main__":
    app = ApplicationBuilder().token("8630478159:AAHjpuWY-NZZ7mTKWK3kLgE8NQokd3dm32Y").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather))

    print("Bot is running...")
    app.run_polling()