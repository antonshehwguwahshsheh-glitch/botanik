import telebot
import phonenumbers
from phonenumbers import carrier, geocoder
from flask import Flask
from threading import Thread
import requests
import random
import string
import hashlib

app = Flask('')
@app.route('/')
def home(): return "Бот жив!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# ВСТАВЬ СЮДА ТОКЕН СТАРОГО БОТА (который работает)
TOKEN = '9158579329:AAFeT1iNKmaVXcuW63BoaMfJK5CZ8C0Wsr4'
bot = telebot.TeleBot(TOKEN)

# --- ГЛАВНОЕ МЕНЮ ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        "📁 CFG", "🔍 Пробив", "🎮 Поиск в играх",
        "🎲 Рандом", "🌐 IP Инфо", "🔑 Пароль",
        "🛡️ Проверка пароля", "📖 Инструкция", "📹 Скачать видео",
        "🛡️ CVE Поиск", "🔓 Temp Root", "📢 Канал", 
        "🆘 Поддержка", "💎 Донат"
    ]
    for i in range(0, len(buttons), 2):
        if i+1 < len(buttons):
            markup.add(buttons[i], buttons[i+1])
        else:
            markup.add(buttons[i])
    
    text = "Привет! Это создатель тгк micro_soft_orig.\nВыбирай действие на клавиатуре:"
    bot.send_message(message.chat.id, text, reply_markup=markup)

# --- TEMP ROOT ---
@bot.message_handler(func=lambda message: message.text == "🔓 Temp Root")
def send_root_files(message):
    instruction = (
        "⚠️ **Внимание!**\n"
        "Перед установкой обязательно переименуйте скачанный файл из **.txt** обратно в **.apk**!"
    )
    
    try:
        filename1 = "KernelSU_v3.3.1_32680-release.txt" 
        with open(filename1, 'rb') as f:
            bot.send_document(message.chat.id, f, caption=f"Файл 1: KernelSU\n\n{instruction}", parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, f"⚠️ Ошибка: файл {filename1} не найден.")

    try:
        filename2 = "dirtyfrag.txt"
        with open(filename2, 'rb') as f:
            bot.send_document(message.chat.id, f, caption=f"Файл 2: DirtyFrag\n\n{instruction}", parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, f"⚠️ Ошибка: файл {filename2} не найден.")

# --- CFG ---
@bot.message_handler(func=lambda message: message.text == "📁 CFG")
def cfg_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Legit", "Rage", "Назад")
    bot.send_message(message.chat.id, "Выбери конфиг:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Legit", "Rage"])
def send_file(message):
    instruction = "⚠️ Переименуйте файл из .txt на .cfg"
    if message.text == "Legit":
        filename = "legit.txt" 
        caption = f"Твой Legit CFG.\n\n{instruction}"
    elif message.text == "Rage":
        filename = "rage.txt" 
        caption = f"Твой Rage CFG.\n\n{instruction}"
    try:
        with open(filename, 'rb') as f:
            bot.send_document(message.chat.id, f, caption=caption, parse_mode='Markdown')
            start(message)
    except Exception:
        bot.send_message(message.chat.id, f"⚠️ Ошибка: файл {filename} не найден.")

# --- ОСТАЛЬНЫЕ КНОПКИ ---
@bot.message_handler(func=lambda message: message.text == "📖 Инструкция")
def instruction(message):
    bot.send_message(message.chat.id, "📖 **Инструкция:**\n1. Скачай файл.\n2. Переименуй `.txt` в `.cfg` или `.apk`.\n3. Закинь в игру или установи.", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == "🛡️ Проверка пароля")
def ask_pass(message):
    bot.send_message(message.chat.id, "Отправь пароль (ответом на это сообщение), и я проверю, был ли он слит.")

@bot.message_handler(func=lambda message: message.text == "🎮 Поиск в играх")
def ask_nick(message):
    bot.send_message(message.chat.id, "Отправь ник. Я дам ссылки на статистику.")

@bot.message_handler(func=lambda message: message.text == "📹 Скачать видео")
def ask_video(message):
    bot.send_message(message.chat.id, "Кинь ссылку на TikTok или YouTube.")

@bot.message_handler(func=lambda message: message.text == "🎲 Рандом")
def ask_random(message):
    bot.send_message(message.chat.id, "Напиши два числа через пробел (например: 1 100).")

@bot.message_handler(func=lambda message: message.text == "🌐 IP Инфо")
def ask_ip(message):
    bot.send_message(message.chat.id, "Отправь IP-адрес (например, 8.8.8.8).")

@bot.message_handler(func=lambda message: message.text == "🔑 Пароль")
def generate_pass(message):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(chars) for _ in range(12))
    bot.send_message(message.chat.id, f"Твой пароль:\n`{password}`", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == "📢 Канал")
def links(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("📢 Telegram", url="https://t.me/Micro_soft_orig"))
    markup.add(telebot.types.InlineKeyboardButton("▶️ YouTube", url="https://www.youtube.com/@nirok25f"))
    bot.send_message(message.chat.id, "Подписывайся!", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🆘 Поддержка")
def support(message):
    bot.send_message(message.chat.id, "Админ: @tg_micro_soft")

@bot.message_handler(func=lambda message: message.text == "💎 Донат")
def donate(message):
    bot.send_message(message.chat.id, "Поддержать автора: https://www.donationalerts.com/r/твой_ник")

@bot.message_handler(func=lambda message: message.text == "🛡️ CVE Поиск")
def ask_cve(message):
    bot.send_message(message.chat.id, "Отправь название программы (например: Windows, Chrome), и я найду уязвимости.")

@bot.message_handler(func=lambda message: message.text == "Назад")
def back(message):
    start(message)

# --- ОБРАБОТКА ВСЕГО ОСТАЛЬНОГО ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text.strip()
    
    if text in ["📁 CFG", "🔍 Пробив", "🎮 Поиск в играх", "🎲 Рандом", "🌐 IP Инфо", "🔑 Пароль", "🛡️ Проверка пароля", "📖 Инструкция", "📹 Скачать видео", "🛡️ CVE Поиск", "🔓 Temp Root", "📢 Канал", "🆘 Поддержка", "💎 Донат", "Legit", "Rage", "Назад"]:
        return

    if text.replace(" ", "").isdigit() and " " in text:
        try:
            a, b = map(int, text.split())
            if a > b: a, b = b, a
            bot.reply_to(message, f"🎲 Случайное число: **{random.randint(a, b)}**", parse_mode='Markdown')
            return
        except: pass

    if message.reply_to_message and "пароль" in message.reply_to_message.text.lower():
        sha1 = hashlib.sha1(text.encode()).hexdigest().upper()
        try:
            r = requests.get(f"https://api.pwnedpasswords.com/range/{sha1[:5]}", timeout=5)
            if sha1[5:] in r.text:
                bot.reply_to(message, "🚨 **Пароль найден в утечках!**")
            else:
                bot.reply_to(message, "✅ **Пароль чист.**")
        except: bot.reply_to(message, "⚠️ Ошибка.")
        return

    if "tiktok.com" in text or "youtube.com" in text or "youtu.be" in text:
        bot.reply_to(message, "⚠️ Скачивание на бесплатном сервере может не работать.")
        return

    if len(text) > 3 and not text.startswith('@') and not text.startswith('+') and not message.reply_to_message:
        try:
            url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={text}&resultsPerPage=2"
            r = requests.get(url, timeout=10)
            data = r.json()
            if "vulnerabilities" in data and data["vulnerabilities"]:
                res = f"🛡️ **Уязвимости для {text}:**\n"
                for item in data["vulnerabilities"]:
                    cve = item["cve"]
                    res += f"• {cve['id']}: {cve['descriptions'][0]['value'][:80]}...\n"
                bot.reply_to(message, res, parse_mode='Markdown')
                return
        except: pass

    if len(text) < 20 and not text.startswith('@') and not text.startswith('+'):
        res = f"🎮 **Игрок:** {text}\n• [Standoff 2](https://standoff2.com/)\n• [PUBG Mobile](https://www.pubg.com/)"
        bot.reply_to(message, res, parse_mode='Markdown', disable_web_page_preview=True)
        return

    if text.startswith('@'):
        username = text.replace('@', '')
        res = f"👤 **Юзернейм:** {text}\n🔗 [TG](https://t.me/{username}) | [VK](https://vk.com/{username})"
        bot.reply_to(message, res, parse_mode='Markdown', disable_web_page_preview=True)
        return

    if text.count('.') == 3 and not text.startswith('+') and not text.startswith('7'):
        try:
            r = requests.get(f"http://ip-api.com/json/{text}?lang=ru", timeout=5).json()
            if r['status'] == 'success':
                res = f"🌐 **IP:** {text}\n🏳️ {r.get('country')}\n📍 {r.get('city')}\n🏢 {r.get('isp')}"
                bot.reply_to(message, res, parse_mode='Markdown')
        except: bot.reply_to(message, "⚠️ Ошибка.")
        return

    try:
        num = phonenumbers.parse(text, "RU")
        if not phonenumbers.is_valid_number(num):
            bot.reply_to(message, "❌ Невалидный номер.")
            return
        operator = carrier.name_for_number(num, "ru") or "Неизвестно"
        region = geocoder.description_for_number(num, "ru") or "Неизвестно"
        clean = text.replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if clean.startswith("8"): clean = "7" + clean[1:]
        res = f"📱 **{text}** | {operator} | {region}\n🔗 [TG](https://t.me/+{clean}) | [WA](https://wa.me/{clean}) | [VK](https://vk.com/search?c%5Bq%5D={clean})"
        bot.reply_to(message, res, parse_mode='Markdown', disable_web_page_preview=True)
    except:
        bot.reply_to(message, "⚠️ Введи номер (+7...), IP или @username.")

if __name__ == "__main__":
    keep_alive()
    print("Бот запущен...")
    bot.polling()rint("Бот запущен...")
    bot.polling()ли @username.")

if __name__ == "__main__":
    keep_alive()
    print("Бот запущен...")
    bot.polling()
