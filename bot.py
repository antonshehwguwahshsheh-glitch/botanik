import telebot
import phonenumbers
from phonenumbers import carrier, geocoder
from flask import Flask
from threading import Thread
import requests
from bs4 import BeautifulSoup

app = Flask('')
@app.route('/')
def home(): return "Бот жив!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

TOKEN = '9089789177:AAGtEvRBco6EpE0MkGEVDhO1ZXECzhxkoyU'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Скинь номер, и я проверю его по открытым источникам.")

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

        # Формируем базовый ответ
        result = f"📱 {text} | {operator} | {region}\n"
        
        # Пытаемся найти имя в Telegram (через web-превью)
        result += f"👤 **Профили (жми, чтобы увидеть имя):**\n"
        result += f"• [Telegram](https://t.me/+{clean})\n"
        result += f"• [WhatsApp](https://wa.me/{clean})\n"
        result += f"• [VK](https://vk.com/search?c%5Bq%5D={clean})\n"
        
        # Ссылка на поиск по базам в Google
        result += f"\n🕵️ [Поиск упоминаний в Google](https://www.google.com/search?q=%22{clean}%22)"
        
        bot.reply_to(message, result, parse_mode='Markdown', disable_web_page_preview=True)
        
    except Exception as e:
        bot.reply_to(message, "⚠️ Ошибка. Введи номер в формате +7...")

if __name__ == "__main__":
    keep_alive()
    print("Бот запущен...")
    bot.polling()
