
import telebot, random, requests
from telebot.types import *
from googletrans import Translator
from dotenv import load_dotenv
import os
from data import get_cat_facts, get_cat_breeds

load_dotenv()
# Твій токен бота від BotFather
TOKEN = os.getenv('token')
bot = telebot.TeleBot(TOKEN)

# Ініціалізація перекладача
translator = Translator()

# Функція для отримання порад з API
def get_cat_advice():
    url = "https://meowfacts.herokuapp.com/"  # API для котячих фактів
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", ["Не вдалося отримати пораду."])[0]  # Повертаємо пораду
        else:
            return "Вибачте, не вдалося отримати пораду."
    except Exception as e:
        return f"Сталася помилка: {str(e)}"

# Список порад для котів як резервний варіант
advice_list = [
    "Не забувайте чистити шерсть кота, щоб уникнути ковтунів!",
    "Переконайтесь, що у кота завжди є чиста вода для пиття.",
    "Щоб уникнути стресу, коти потребують власного простору та притулку.",
    "Регулярно відвідуйте ветеринара для профілактики хвороб.",
    "Грайте з котом щодня, щоб підтримати його фізичну активність."
]

# Функція для перекладу тексту на українську
def translate_to_ukrainian(text):
    # Ensure the text is encoded to UTF-8
    text = text.encode('utf-8').decode('utf-8')
    
    translator = Translator()
    try:
        # Translate from English to Ukrainian
        translation = translator.translate(text, src='en', dest='uk')
        return translation.text
    except Exception as e:
        return f"Не вдалося перекласти: {str(e)}"
# Стартова команда
@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.reply_to(
        message,
        "Привіт! Я твій помічник для власників котів. Ось що я можу зробити:\n"
        "/advice - Щоденні поради\n"
        "/facts - Цікаві факти про котів\n"
        "/food - Рекомендації з харчування\n"
        "/game - Ігри для котів\n"
        "/breeds - Каталог порід котів"
    )

# Команда для отримання порад
@bot.message_handler(commands=['advice'])
def advice(message: Message):
    # Спробуємо отримати пораду з API, якщо не вийде — використаємо резервну пораду
    cat_advice = get_cat_advice()
    translated_advice = translate_to_ukrainian(cat_advice)
    bot.reply_to(message, f"Сьогоднішня порада: {translated_advice}")

# Команда для фактів про котів
@bot.message_handler(commands=['facts'])
def facts(message: Message):
    facts = get_cat_facts()
    if facts:
        random_fact = random.choice(facts)  # Вибір випадкового факту
        translated_fact = translate_to_ukrainian(random_fact)
        bot.send_message(message.chat.id, f"Факт: {translated_fact}")
    else:
        bot.send_message(message.chat.id, "Не вдалося отримати дані про породи котів. Спробуйте пізніше.")

# Команда для рекомендацій з харчування
    #@bot.message_handler(commands=['food'])
    #def food(message: Message):
        #food_recommendations = get_food_recommendations()
       # bot.reply_to(message, "\n".join(food_recommendations))

# Команда для ігор
@bot.message_handler(commands=['game'])
def game(message: Message):
    bot.reply_to(message, "Лазерний покажчик: рухайте пальцем по екрану!")

# Команда для отримання порід котів
@bot.message_handler(commands=['breeds'])
def breeds(message: Message):
    breeds = get_cat_breeds()
    if breeds:
        random_breed = random.choice(breeds)  # Вибір випадкової породи
        bot.send_message(message.chat.id, f"Сьогоднішня порода: {random_breed}")
    else:
        bot.send_message(message.chat.id, "Не вдалося отримати дані про породи котів. Спробуйте пізніше.")

# Обробка невідомих команд
@bot.message_handler(func=lambda message: True)
def unknown(message: Message):
    bot.reply_to(message, "Вибачте, я не розумію цю команду.")

# Запуск бота
if __name__ == '__main__':
    print("Bot is running...")
    bot.polling()
