import telebot, random, requests, os
from telebot.types import Message
from flask import Flask, request
from googletrans import Translator
from dotenv import load_dotenv
from data import get_cat_facts, get_cat_breeds

load_dotenv()

TOKEN = os.getenv('TOKEN')  # Make sure it's uppercase in Render!
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your-render-app.onrender.com/' + TOKEN)  # Replace with your Render app name!
    return "Webhook set!", 200

translator = Translator()

def get_cat_advice():
    url = "https://meowfacts.herokuapp.com/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", ["Не вдалося отримати пораду."])[0]
        else:
            return "Вибачте, не вдалося отримати пораду."
    except Exception as e:
        return f"Сталася помилка: {str(e)}"

advice_list = [
    "Не забувайте чистити шерсть кота, щоб уникнути ковтунів!",
    "Переконайтесь, що у кота завжди є чиста вода для пиття.",
    "Щоб уникнути стресу, коти потребують власного простору та притулку.",
    "Регулярно відвідуйте ветеринара для профілактики хвороб.",
    "Грайте з котом щодня, щоб підтримати його фізичну активність."
]

def translate_to_ukrainian(text):
    try:
        translation = translator.translate(text, src='en', dest='uk')
        return translation.text
    except Exception as e:
        return f"Не вдалося перекласти: {str(e)}"

@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.reply_to(
        message,
        "Привіт! Я твій помічник для власників котів. Ось що я можу зробити:\n"
        "/advice - Щоденні поради\n"
        "/facts - Цікаві факти про котів\n"
        "/game - Ігри для котів\n"
        "/breeds - Каталог порід котів"
    )

@bot.message_handler(commands=['advice'])
def advice(message: Message):
    cat_advice = get_cat_advice()
    translated_advice = translate_to_ukrainian(cat_advice)
    bot.reply_to(message, f"Сьогоднішня порада: {translated_advice}")

@bot.message_handler(commands=['facts'])
def facts(message: Message):
    facts = get_cat_facts()
    if facts:
        random_fact = random.choice(facts)
        translated_fact = translate_to_ukrainian(random_fact)
        bot.send_message(message.chat.id, f"Факт: {translated_fact}")
    else:
        bot.send_message(message.chat.id, "Не вдалося отримати дані про породи котів. Спробуйте пізніше.")

@bot.message_handler(commands=['game'])
def game(message: Message):
    bot.reply_to(message, "Лазерний покажчик: рухайте пальцем по екрану!")

@bot.message_handler(commands=['breeds'])
def breeds(message: Message):
    breeds = get_cat_breeds()
    if breeds:
        random_breed = random.choice(breeds)
        random_breed = translate_to_ukrainian(random_breed)
        bot.send_message(message.chat.id, f"Сьогоднішня порода: {random_breed}")
    else:
        bot.send_message(message.chat.id, "Не вдалося отримати дані про породи котів. Спробуйте пізніше.")

@bot.message_handler(func=lambda message: True)
def unknown(message: Message):
    bot.reply_to(message, "Вибачте, я не розумію цю команду.")

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
