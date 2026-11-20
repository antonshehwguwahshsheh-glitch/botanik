import telebot
import phonenumbers
from phonenumbers import carrier, geocoder
from flask import Flask
from threading import Thread
import requests
import re

app = Flask('')
@app.route('/')
def home(): return "Бот жив!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

TOKEN = '9089789177:AAGtEvRBco6EpE0MkGEVDhO1ZXECzhxkoyU'
bot = telebot.TeleBot(TOKEN)

def get_tg_name(phone):
    # Пытаемся получить имя из публичной страницы Telegram
    try:
        clean = phone.replace("+", "").replace(" ", "").replace("-", "")
        if clean.startswith("8"): clean = "7" + clean[1:]
        url = f"https://t.me/+{clean}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        r = requests.get(url, headers=headers, timeout=5)
        # Ищем имя в мета-теге og:title
        match = re.search(r'<meta property="og:title" content="(.*?)"', r.text)
        if match:
            name = match.group(1)
            # Отсекаем "Telegram" или другие мусорные слова
            if name.lower() not in ['telegram', 'telegram messenger']:
                return name
    except Exception:
        pass
    return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Скинь номер, я попробую найти имя и соцсети.")

@bot.message_handler(func=lambda message: True)
def lookup(message):
    text = message.text.strip()
    try:
        num = phonenumbers.parse(text, "RU")
        if not phonenumbers.is_valid_number(num):
            bot.reply_to(message, "❌ Невалидный номер.")
            return
            
        operator = carrier.name_for_number(num, "ru") or "Неизвестно"
        region = geocoder.description_for_number(num, "ru") or "Неизвестно"
        clean = text.replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if clean.startswith("8"): clean = "7" + clean[1:]

        # Пытаемся найти имя
        tg_name = get_tg_name(text)
        
        result = f"📱 {text} | {operator} | {region}\n"
        if tg_name:
            result += f"👤 **Имя (из Telegram):** {tg_name}\n"
        else:
            result += f"👤 **Имя:** Скрыто или не найдено\n"
            
        result += (
            f"\n🔗 **Ссылки:**\n"
            f"[TG](https://t.me/+{clean}) | [WA](https://wa.me/{clean}) | "
            f"[VK](https://vk.com/search?c%5Bq%5D={clean}) | "
            f"[Авито](https://www.avito.ru/all?q={clean}) | [Google](https://www.google.com/search?q=%22{clean}%22)"
        )
        
        bot.reply_to(message, result, parse_mode='Markdown', disable_web_page_preview=True)
        
    except Exception as e:
        bot.reply_to(message, "⚠️ Ошибка. Введи номер в формате +7...")

if __name__ == "__main__":
    keep_alive()
    print("Бот запущен...")
    bot.polling()
