import telebot
import phonenumbers
from phonenumbers import carrier, geocoder
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "Бот жив!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# Твой токен
TOKEN = '9158579329:AAFeT1iNKmaVXcuW63BoaMfJK5CZ8C0Wsr4'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    # Главное меню (внизу экрана)
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_cfg = telebot.types.KeyboardButton("📁 Получить CFG")
    btn_probit = telebot.types.KeyboardButton("🔍 Пробив")
    markup.add(btn_cfg, btn_probit)
    
    text = (
        "Привет! Это создатель тгк micro_soft_orig.\n"
        "Я выдаю CFG для Zenin и пробиваю номера.\n"
        "Выбирай действие на клавиатуре:"
    )
    bot.send_message(message.chat.id, text, reply_markup=markup)

# --- МЕНЮ ВЫБОРА КФГ (ТЕПЕРЬ ВНИЗУ) ---
@bot.message_handler(func=lambda message: message.text == "📁 Получить CFG")
def cfg_menu(message):
    # Меняем клавиатуру на выбор Legit или Rage
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_legit = telebot.types.KeyboardButton("Legit")
    btn_rage = telebot.types.KeyboardButton("Rage")
    btn_back = telebot.types.KeyboardButton("Назад")
    markup.add(btn_legit, btn_rage)
    markup.add(btn_back)
    
    bot.send_message(message.chat.id, "Выбери конфиг (Legit или Rage):", reply_markup=markup)

# --- ОТПРАВКА ФАЙЛА ---
@bot.message_handler(func=lambda message: message.text in ["Legit", "Rage"])
def send_file(message):
    instruction = "⚠️ **Внимание!**\nПеред установкой кфг обязательно переименуйте файл из **.txt** на **.cfg**"
    
    if message.text == "Legit":
        filename = "legit.txt" 
        caption = f"Твой Legit CFG.\n\n{instruction}"
    elif message.text == "Rage":
        filename = "rage.txt" 
        caption = f"Твой Rage CFG.\n\n{instruction}"
    
    try:
        with open(filename, 'rb') as f:
            bot.send_document(message.chat.id, f, caption=caption, parse_mode='Markdown')
            
            # Возвращаем главное меню после отправки
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(telebot.types.KeyboardButton("📁 Получить CFG"), telebot.types.KeyboardButton("🔍 Пробив"))
            bot.send_message(message.chat.id, "Что-то еще?", reply_markup=markup)
            
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ошибка: файл {filename} не найден на сервере.")

# --- КНОПКА НАЗАД ---
@bot.message_handler(func=lambda message: message.text == "Назад")
def back_to_main(message):
    start(message)

# --- ПРОБИВ ---
@bot.message_handler(func=lambda message: message.text == "🔍 Пробив")
def ask_phone(message):
    bot.send_message(message.chat.id, "Отправь мне номер телефона (например, +7999...) или @username.")

@bot.message_handler(func=lambda message: True)
def lookup(message):
    text = message.text.strip()
    
    # Игнорируем системные кнопки
    if text in ["📁 Получить CFG", "🔍 Пробив", "Legit", "Rage", "Назад"]:
        return

    # Юзернейм
    if text.startswith('@'):
        username = text.replace('@', '')
        result = f"👤 **Поиск по юзернейму:** {text}\n\n"
        result += f"🔗 **Ссылки:**\n"
        result += f"• [Telegram](https://t.me/{username})\n"
        result += f"• [VK](https://vk.com/{username})\n"
        result += f"• [Instagram](https://instagram.com/{username})\n"
        bot.reply_to(message, result, parse_mode='Markdown', disable_web_page_preview=True)
        return

    # Номер
    try:
        num = phonenumbers.parse(text, "RU")
        if not phonenumbers.is_valid_number(num):
            bot.reply_to(message, "❌ Невалидный номер.")
            return
            
        operator = carrier.name_for_number(num, "ru") or "Неизвестно"
        region = geocoder.description_for_number(num, "ru") or "Неизвестно"
        clean = text.replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if clean.startswith("8"): clean = "7" + clean[1:]

        result = f"📱 **Номер:** {text}\n"
        result += f"🏢 **Оператор:** {operator}\n"
        result += f"🌍 **Регион:** {region}\n\n"
        result += (
            f"🔗 **Ссылки для проверки:**\n"
            f"• [Telegram](https://t.me/+{clean})\n"
            f"• [WhatsApp](https://wa.me/{clean})\n"
            f"• [VK](https://vk.com/search?c%5Bq%5D={clean})\n"
            f"• [Авито](https://www.avito.ru/all?q={clean})\n"
            f"• [Google](https://www.google.com/search?q=%22{clean}%22)"
        )
        bot.reply_to(message, result, parse_mode='Markdown', disable_web_page_preview=True)
        
    except Exception as e:
        bot.reply_to(message, "⚠️ Введи номер в формате +7... или @username.")

if __name__ == "__main__":
    keep_alive()
    print("Бот запущен...")
    bot.polling()
