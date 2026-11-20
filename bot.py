import telebot
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from flask import Flask
from threading import Thread
import requests

app = Flask('')
@app.route('/')
def home(): return "Бот жив!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

TOKEN = '9089789177:AAGtEvRBco6EpE0MkGEVDhO1ZXECzhxkoyU'
bot = telebot.TeleBot(TOKEN)

def get_social_links(phone):
    # Форматируем номер для разных соцсетей
    clean = phone.replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if clean.startswith("8"): clean = "7" + clean[1:]
    
    return (
        f"🔗 **Проверка соцсетей:**\n"
        f"• [Telegram](https://t.me/+{clean})\n"
        f"• [WhatsApp](https://wa.me/{clean})\n"
        f"• [VK (возможно)](https://vk.com/search?c%5Bq%5D={clean})\n"
        f"• [OK (возможно)](https://ok.ru/search?st.query={clean})\n\n"
        f"🕵️ **Поиск в базах (Google):**\n"
        f"[Искать ФИО и упоминания](https://www.google.com/search?q=%22{clean}%22+ФИО+Имя+Адрес)\n"
    )

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я OSINT-бот. Скинь номер телефона (например, +79161234567), и я проверю его по открытым источникам и соцсетям.")

@bot.message_handler(func=lambda message: True)
def lookup(message):
    text = message.text.strip()
    try:
        num = phonenumbers.parse(text, "RU")
        if not phonenumbers.is_valid_number(num):
            bot.reply_to(message, "❌ Номер невалиден.")
            return
            
        operator = carrier.name_for_number(num, "ru")
        region = geocoder.description_for_number(num, "ru")
        
        # Формируем ответ
        result = f"📱 **Номер:** {text}\n"
        result += f"🏢 **Оператор:** {operator if operator else 'Неизвестно'}\n"
        result += f"🌍 **Регион:** {region if region else 'Неизвестно'}\n\n"
        result += get_social_links(text)
        
        bot.reply_to(message, result, parse_mode='Markdown', disable_web_page_preview=True)
    except Exception as e:
        bot.reply_to(message, "⚠️ Ошибка. Введи номер в формате +7XXXXXXXXXX")

if __name__ == "__main__":
    keep_alive()
    print("Бот запущен...")
    bot.polling()
