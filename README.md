# Telegram Bot Deployment Guide

## 🚀 Overview
This guide provides step-by-step instructions to set up and deploy a Telegram bot on **Render** using **Flask** as a web server.

## 📌 Prerequisites
Before you start, ensure you have the following:
- A **Telegram bot token** from [@BotFather](https://t.me/BotFather)
- A **Render** account ([Sign up](https://render.com/))
- Installed dependencies: Python 3.x, `pip`, `virtualenv`
- `git` installed on your system

---

## 📥 1. Clone the Repository
```sh
$ git clone https://github.com/your-repository/telegram-bot.git
$ cd telegram-bot
```

## 📦 2. Install Dependencies
Create a virtual environment and install required packages:
```sh
$ python -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate
$ pip install -r requirements.txt
```

### 📜 **requirements.txt** should include:
```
pyTelegramBotAPI
googletrans==4.0.0-rc1
python-dotenv
requests
Flask
gunicorn
waitress
```

---

## 🔑 3. Set Up Environment Variables
Create a `.env` file in the root directory and add:
```
token=YOUR_TELEGRAM_BOT_TOKEN
```

Example `.env` file:
```
token=1234567890:ABCDEF1234567890abcdef1234567890
```

---

## 📝 4. Update `bot.py`
Ensure your `bot.py` contains webhook logic:
```python
import telebot, requests, os
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('token')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@app.route('/')
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your-app-name.onrender.com/' + TOKEN)
    return "Webhook set!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## 🚀 5. Deploy on Render
### 1️⃣ **Create a new Web Service on Render**
- Go to [Render](https://dashboard.render.com/)
- Click **"New"** → **"Web Service"**
- Connect your **GitHub repo**
- Choose **Python** as environment
- Set **Build Command**: `pip install -r requirements.txt`
- Set **Start Command**: `waitress-serve --host=0.0.0.0 --port=5000 bot:app`
- Click **Deploy**

### 2️⃣ **Set Environment Variables**
- Go to **Render Dashboard** → Your Web Service
- Click **"Environment"**
- Add `token=YOUR_TELEGRAM_BOT_TOKEN`

### 3️⃣ **Set Telegram Webhook**
After deployment, set the webhook by running:
```sh
curl "https://api.telegram.org/botYOUR_TELEGRAM_BOT_TOKEN/setWebhook?url=https://your-app-name.onrender.com/YOUR_TELEGRAM_BOT_TOKEN"
```
Example:
```sh
curl "https://api.telegram.org/bot1234567890:ABCDEF1234567890abcdef1234567890/setWebhook?url=https://my-bot.onrender.com/1234567890:ABCDEF1234567890abcdef1234567890"
```

---

## 🔄 6. Testing the Bot
Send `/start` to your bot in Telegram and see if it responds!

### ✅ **Check Webhook Status**
Run this to verify if Telegram is sending updates:
```sh
curl "https://api.telegram.org/botYOUR_TELEGRAM_BOT_TOKEN/getWebhookInfo"
```

---

## 🛠 Troubleshooting
### ❌ Bot doesn’t respond?
- Check logs on Render: **"Logs" Tab**
- Restart Web Service
- Run webhook setup again

### ❌ Webhook not set?
Reset it:
```sh
curl "https://api.telegram.org/botYOUR_TELEGRAM_BOT_TOKEN/deleteWebhook"
```

---

## 🎉 Done!
Your Telegram bot is now live and running on Render! 🚀

