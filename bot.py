import telebot
import phonenumbers
from phonenumbers import carrier, geocoder
from flask import Flask
from threading import Thread
import requests
import random
import string

app = Flask('')
@app.route('/')
def home(): return "Бот жив!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# Твой токен
TOKEN = '9158579329:AAFeT1iNKmaVXcuW63BoaMfJK5CZ8C0Wsr4'
bot = telebot.TeleBot(TOKEN)

# --- ГЛАВНОЕ МЕНЮ ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_cfg = telebot.types.KeyboardButton("📁 Получить CFG")
    btn_probit = telebot.types.KeyboardButton("🔍 Пробив")
    btn_ip = telebot.types.KeyboardButton("🌐 IP Инфо")
    btn_pass = telebot.types.KeyboardButton("🔑 Пароль")
    btn_links = telebot.types.KeyboardButton("📢 Наш канал")
    btn_support = telebot.types.KeyboardButton("🆘 Поддержка")
    
    markup.add(btn_cfg, btn_probit)
    markup.add(btn_ip, btn_pass)
    markup.add(btn_links, btn_support)
    
    text = (
        "Привет! Это создатель тгк micro_soft_orig.\n"
        "Выбирай действие на клавиатуре ниже:"
    )
    bot.send_message(message.chat.id, text, reply_markup=markup)

# --- CFG ---
@bot.message_handler(func=lambda message: message.text == "📁 Получить CFG")
def cfg_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_legit = telebot.types.KeyboardButton("Legit")
    btn_rage = telebot.types.KeyboardButton("Rage")
    btn_back = telebot.types.KeyboardButton("Назад")
    markup.add(btn_legit, btn_rage)
    markup.add(btn_back)
    bot.send_message(message.chat.id, "Выбери конфиг (Legit или Rage):", reply_markup=markup)

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
            # Возвращаем меню
            start(message)
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ошибка: файл {filename} не найден на сервере.")

# --- ПРОБИВ ---
@bot.message_handler(func=lambda message: message.text == "🔍 Пробив")
def ask_phone(message):
    bot.send_message(message.chat.id, "Отправь мне номер телефона (например, +7999...) или @username.")

# --- IP ИНФО ---
@bot.message_handler(func=lambda message: message.text == "🌐 IP Инфо")
def ask_ip(message):
    bot.send_message(message.chat.id, "Отправь мне IP-адрес (например, 8.8.8.8).")

# --- ПАРОЛЬ ---
@bot.message_handler(func=lambda message: message.text == "🔑 Пароль")
def generate_pass(message):
    # Генерируем пароль из 12 символов
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(chars) for _ in range(12))
    bot.send_message(message.chat.id, f"Твой новый сложный пароль:\n`{password}`", parse_mode='Markdown')

# --- ССЫЛКИ ---
@bot.message_handler(func=lambda message: message.text == "📢 Наш канал")
def links(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("📢 Telegram Канал", url="https://t.me/Micro_soft_orig"))
    markup.add(telebot.types.InlineKeyboardButton("▶️ YouTube", url="https://www.youtube.com/@nirok25f"))
    bot.send_message(message.chat.id, "Подписывайся, чтобы не пропустить новые кфг и читы!", reply_markup=markup)

# --- ПОДДЕРЖКА ---
@bot.message_handler(func=lambda message: message.text == "🆘 Поддержка")
def support(message):
    bot.send_message(message.chat.id, "По всем вопросам пиши админу: @tg_micro_soft")

# --- НАЗАД ---
@bot.message_handler(func=lambda message: message.text == "Назад")
def back(message):
    start(message)

# --- ОБРАБОТКА ТЕКСТА (Номер, Юзернейм, IP) ---
@bot.message_handler(func=lambda message: True)
def lookup(message):
    text = message.text.strip()
    
    # Игнорируем кнопки
    if text in ["📁 Получить CFG", "🔍 Пробив", "Legit", "Rage", "Назад", "🌐 IP Инфо", "🔑 Пароль", "📢 Наш канал", "🆘 Поддержка"]:
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

    # IP-адрес
    if text.count('.') == 3 and not text.startswith('+') and not text.startswith('7'):
        try:
            r = requests.get(f"http://ip-api.com/json/{text}?lang=ru", timeout=5).json()
            if r['status'] == 'success':
                result = (
                    f"🌐 **IP:** {text}\n"
                    f"🏳️ **Страна:** {r.get('country', 'Неизвестно')}\n"
                    f"📍 **Город:** {r.get('city', 'Неизвестно')}\n"
                    f"🏢 **Провайдер:** {r.get('isp', 'Неизвестно')}"
                )
                bot.reply_to(message, result, parse_mode='Markdown')
            else:
                bot.reply_to(message, "❌ Не удалось найти информацию по этому IP.")
        except:
            bot.reply_to(message, "⚠️ Ошибка при проверке IP.")
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
        bot.reply_to(message, "⚠️ Введи номер в формате +7... или @username, или IP.")

if __name__ == "__main__":
    keep_alive()
    print("Бот запущен...")
    bot.polling()
