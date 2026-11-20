import telebot
import phonenumbers
from phonenumbers import carrier, geocoder
from flask import Flask
from threading import Thread
import requests
from bs4 import BeautifulSoup
import re

app = Flask('')
@app.route('/')
def home(): return "Бот жив!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

TOKEN = '9089789177:AAGtEvRBco6EpE0MkGEVDhO1ZXECzhxkoyU'
bot = telebot.TeleBot(TOKEN)

# Функция для поиска в Google (вытаскиваем имена из открытых источников)
def search_google(phone):
    try:
        clean = phone.replace("+", "").replace(" ", "").replace("-", "")
        if clean.startswith("8"): clean = "7" + clean[1:]
        url = f"https://www.google.com/search?q=%22{clean}%22"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=5)
        
        # Ищем имена (кириллица, 2-3 слова)
        names = re.findall(r'[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+){1,2}', r.text)
        if names:
            return list(set(names))[:3] # Возвращаем до 3 уникальных имен
    except:
        pass
    return []

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Скинь номер, и я поищу ФИО в открытых базах и на сайтах.")

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

        # Ищем имена в Google
        found_names = search_google(text)
        
        result = f"📱 {text} | {operator} | {region}\n"
        
        if found_names:
            result += f"👤 **Найденные имена (Google):**\n"
            for name in found_names:
                result += f"• {name}\n"
        else:
            result += f"👤 **Имена:** В открытых источниках не найдено.\n"
            
        result += (
            f"\n🔗 **Ссылки:**\n"
            f"[TG](https://t.me/+{clean}) | [WA](https://wa.me/{clean}) | "
            f"[VK](https://vk.com/search?c%5Bq%5D={clean}) | "
            f"[Авито](https://www.avito.ru/all?q={clean})"
        )
        
        bot.reply_to(message, result, parse_mode='Markdown', disable_web_page_preview=True)
        
    except Exception as e:
        bot.reply_to(message, "⚠️ Ошибка. Введи номер в формате +7...")

if __name__ == "__main__":
    keep_alive()
    print("Бот запущен...")
    bot.polling()
