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

TOKEN = '9158579329:AAFeT1iNKmaVXcuW63BoaMfJK5CZ8C0Wsr4'
bot = telebot.TeleBot(TOKEN)

# --- ГЛАВНОЕ МЕНЮ ---
@bot.message_handler(commands=['start'])
def start(message):
    channel_text = (
        "👋 **Привет! Это бот канала micro_soft_orig.**\n\n"
        "🔥 **Что мы добавили за всё время:**\n"
        "• Рабочие CFG для Standoff 2 (Legit / Rage)\n"
        "• Скрипты для Temp Root (KernelSU + DirtyFrag)\n"
        "• Пробив по номеру (оператор, регион, соцсети)\n"
        "• Генератор паролей и IP-инфо\n\n"
        "📢 **Подписывайся на наш канал**, чтобы первым получать новые читы, кфг и софт:\n"
        "👉 [t.me/Micro_soft_orig](https://t.me/Micro_soft_orig)\n"
        "▶️ [YouTube канал](https://www.youtube.com/@nirok25f)\n\n"
        "👇 Выбирай действие на клавиатуре ниже:"
    )
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Убрал "ПД" из меню
    buttons = [
        "📁 CFG", "🔍 Пробив",
        "🎲 Рандом", "🌐 IP", "🔑 Генератор",
        "📖 Инструкция", "📹 Видео",
        "🛡️ CVE", "🔓 Temp Root", "📢 Канал", 
        "🆘 Поддержка"
    ]
    for i in range(0, len(buttons), 2):
        if i+1 < len(buttons):
            markup.add(buttons[i], buttons[i+1])
        else:
            markup.add(buttons[i])
    
    bot.send_message(message.chat.id, channel_text, reply_markup=markup, parse_mode='Markdown', disable_web_page_preview=True)

# --- ИНСТРУКЦИЯ С ВИДЕО-ССЫЛКАМИ ---
@bot.message_handler(func=lambda message: message.text == "📖 Инструкция")
def instruction_menu(message):
    markup = telebot.types.InlineKeyboardMarkup()
    
    link_cfg1 = "https://vt.tiktok.com/ZSpKXLwc1/"
    link_cfg2 = "https://vt.tiktok.com/ZSpKX6qcR/"
    link_root = "https://vt.tiktok.com/ZSpKXxHpu/"
    
    markup.add(telebot.types.InlineKeyboardButton("📄 Видео: Установка CFG (1)", url=link_cfg1))
    markup.add(telebot.types.InlineKeyboardButton("📄 Видео: Установка CFG (2)", url=link_cfg2))
    markup.add(telebot.types.InlineKeyboardButton("🔓 Видео: Установка Temp Root", url=link_root))
    
    bot.send_message(message.chat.id, "📖 **Выбери видео-инструкцию:**", reply_markup=markup, parse_mode='Markdown')

# --- CFG ---
@bot.message_handler(func=lambda message: message.text == "📁 CFG")
def cfg_menu(message):
    history_text = (
        "📁 **Конфиги (CFG)**\n\n"
        "Выбери нужный конфиг ниже:\n"
        "— **Legit** (легитный)\n"
        "— **Rage** (агрессивный)"
    )
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # Убрал "ПД"
    markup.add("Legit", "Rage", "Назад")
    bot.send_message(message.chat.id, history_text, reply_markup=markup, parse_mode='Markdown')

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
        bot.send_message(message.chat.id, f"⚠️ Ошибка: файл {filename} не найден на GitHub.")

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

# --- ВИДЕО (Общий профиль TikTok) ---
@bot.message_handler(func=lambda message: message.text == "📹 Видео")
def video_menu(message):
    markup = telebot.types.InlineKeyboardMarkup()
    # ЗАМЕНИ НА СВОЙ НИК В TIKTOK
    markup.add(telebot.types.InlineKeyboardButton("📺 Мой TikTok", url="https://www.tiktok.com/@твой_ник"))
    bot.send_message(message.chat.id, "🎬 **Смотри мои туториалы в TikTok:**", reply_markup=markup)

# --- ОСТАЛЬНЫЕ КНОПКИ ---
@bot.message_handler(func=lambda message: message.text == "🎲 Рандом")
def ask_random(message):
    bot.send_message(message.chat.id, "Напиши два числа через пробел (например: 1 100).")

@bot.message_handler(func=lambda message: message.text == "🌐 IP")
def ask_ip(message):
    bot.send_message(message.chat.id, "Отправь IP-адрес (например, 8.8.8.8).")

@bot.message_handler(func=lambda message: message.text == "🔑 Генератор")
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

@bot.message_handler(func=lambda message: message.text == "🛡️ CVE")
def ask_cve(message):
    bot.send_message(message.chat.id, "Отправь название программы (например: Windows, Chrome), и я найду уязвимости.")

@bot.message_handler(func=lambda message: message.text == "Назад")
def back(message):
    start(message)

# --- ОБРАБОТКА ВСЕГО ОСТАЛЬНОГО ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text.strip()
    
    if text in ["📁 CFG", "🔍 Пробив", "🎲 Рандом", "🌐 IP", "🔑 Генератор", "📖 Инструкция", "📹 Видео", "🛡️ CVE", "🔓 Temp Root", "📢 Канал", "🆘 Поддержка", "Legit", "Rage", "Назад"]:
        return

    if text.replace(" ", "").isdigit() and " " in text:
        try:
            a, b = map(int, text.split())
            if a > b: a, b = b, a
            bot.reply_to(message, f"🎲 Случайное число: **{random.randint(a, b)}**", parse_mode='Markdown')
            return
        except: pass

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

    # Пробив номера (добавил проверку)
    try:
        num = phonenumbers.parse(text, "RU")
        if not phonenumbers.is_valid_number(num):
            bot.reply_to(message, "❌ Невалидный номер. Введи в формате +79991234567")
            return
        operator = carrier.name_for_number(num, "ru") or "Неизвестно"
        region = geocoder.description_for_number(num, "ru") or "Неизвестно"
        clean = text.replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if clean.startswith("8"): clean = "7" + clean[1:]
        res = f"📱 **{text}** | {operator} | {region}\n🔗 [TG](https://t.me/+{clean}) | [WA](https://wa.me/{clean}) | [VK](https://vk.com/search?c%5Bq%5D={clean})"
        bot.reply_to(message, res, parse_mode='Markdown', disable_web_page_preview=True)
    except:
        bot.reply_to(message, "⚠️ Введи номер в формате +79991234567, IP или @username.")

if __name__ == "__main__":
    keep_alive()
    print("Бот запущен...")
    bot.polling()
