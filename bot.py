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

# --- МЕНЮ ВЫБОРА КФГ ---
@bot.message_handler(func=lambda message: message.text == "📁 Получить CFG")
def cfg_menu(message):
    markup = telebot.types.InlineKeyboardMarkup()
    # Кнопки для выбора кфг
    btn_legit = telebot.types.InlineKeyboardButton("🥷 Free Legit CFG", callback_data="get_legit")
    btn_rage = telebot.types.InlineKeyboardButton("🔥 Rage CFG", callback_data="get_rage")
    markup.add(btn_legit, btn_rage)
    
    bot.send_message(message.chat.id, "Выбери нужный конфиг:", reply_markup=markup)

# --- ОТПРАВКА ВЫБРАННОГО ФАЙЛА ---
@bot.callback_query_handler(func=lambda call: call.data.startswith('get_'))
def send_file(call):
    if call.data == "get_legit":
        filename = "free_legit.txt" # Имя файла на GitHub
        caption = "Твой Free Legit CFG. Приятной игры!"
    elif call.data == "get_rage":
        filename = "rage.txt" # Имя файла на GitHub
        caption = "Твой Rage CFG. Будь осторожен!"
    else:
        return

    try:
        with open(filename, 'rb') as f:
            bot.send_document(call.message.chat.id, f, caption=caption)
            bot.answer_callback_query(call.id, "Файл отправлен!")
    except Exception as e:
        bot.answer_callback_query(call.id, "Ошибка: файл не найден.")
        bot.send_message(call.message.chat.id, f"⚠️ Ошибка: убедись, что файл {filename} загружен на GitHub.")

# --- ПРОБИВ ---
@bot.message_handler(func=lambda message: message.text == "🔍 Пробив")
def ask_phone(message):
    bot.send_message(message.chat.id, "Отправь мне номер телефона (например, +7999...) или @username.")

@bot.message_handler(func=lambda message: True)
def lookup(message):
    text = message.text.strip()
    
    # Игнорируем нажатия кнопок
    if text in ["📁 Получить CFG", "🔍 Пробив"]:
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
