import telebot
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from flask import Flask
from threading import Thread

# --- Веб-сервер для Render (чтобы бот не засыпал) ---
app = Flask('')

@app.route('/')
def home():
    return "Бот жив!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Твой токен ---
TOKEN = '9089789177:AAGtEvRBco6EpE0MkGEVDhO1ZXECzhxkoyU'
bot = telebot.TeleBot(TOKEN)

# --- Функция генерации ссылок для поиска ---
def get_search_links(phone):
    # Очищаем номер от плюсов и пробелов для корректного поиска
    clean_phone = phone.replace("+", "").replace(" ", "")
    return (
        f"\n🔍 **Поиск в открытых источниках:**\n"
        f"[Google](https://www.google.com/search?q=%2B{clean_phone}) | "
        f"[Яндекс](https://yandex.ru/search/?text=%2B{clean_phone}) | "
        f"[ВКонтакте](https://vk.com/search?c%5Bq%5D={clean_phone})"
    )

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я твой OSINT-бот. Скинь номер телефона (например, +79161234567), и я пробью его по открытым данным.")

@bot.message_handler(func=lambda message: True)
def lookup(message):
    text = message.text.strip()
    try:
        # Парсим номер (по умолчанию Россия)
        num = phonenumbers.parse(text, "RU")
        
        # Проверяем валидность
        if not phonenumbers.is_valid_number(num):
            bot.reply_to(message, "❌ Номер невалиден. Проверь цифры.")
            return
            
        # Получаем данные об операторе и регионе
        operator = carrier.name_for_number(num, "ru")
        region = geocoder.description_for_number(num, "ru")
        tz = timezone.time_zones_for_number(num)
        
        # Формируем основной текст
        result = f"📱 **Номер:** {text}\n"
        result += f"🏢 **Оператор:** {operator if operator else 'Неизвестно'}\n"
        result += f"🌍 **Регион:** {region if region else 'Неизвестно'}\n"
        result += f"⏰ **Пояс:** {', '.join(tz) if tz else 'Неизвестно'}\n"
        
        # Добавляем ссылки на поиск
        result += get_search_links(text)
        
        # Отправляем сообщение с поддержкой Markdown для ссылок
        bot.reply_to(message, result, parse_mode='Markdown', disable_web_page_preview=True)
        
    except Exception as e:
        bot.reply_to(message, "⚠️ Ошибка. Введи номер в формате +7XXXXXXXXXX")

if __name__ == "__main__":
    keep_alive()
    print("Бот запущен...")
    bot.polling()
