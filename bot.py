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

# Твой новый токен
TOKEN = '9158579329:AAFeT1iNKmaVXcuW63BoaMfJK5CZ8C0Wsr4'
bot = telebot.TeleBot(TOKEN)

# Расширенный поиск имен в Google
def search_google(query):
    names = []
    try:
        url = f"https://www.google.com/search?q=%22{query}%22"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        r = requests.get(url, headers=headers, timeout=7)
        
        # Ищем ФИО, имена, ники (кириллица и латиница)
        found = re.findall(r'[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+){1,2}', r.text)
        found += re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2}', r.text)
        
        # Фильтруем мусор
        for name in found:
            if name not in names and len(name) > 3 and "Google" not in name and "Search" not in name:
                names.append(name)
    except:
        pass
    return names[:3]

@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "Привет это создатель тгк micro_soft_orig\n"
        "Для вас я создал бота для пробивки.\n"
        "Вставь номер телефона или юзер нейм."
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: True)
def lookup(message):
    text = message.text.strip()
    
    # --- ЕСЛИ ВВЕЛИ ЮЗЕРНЕЙМ ---
    if text.startswith('@'):
        username = text.replace('@', '')
        found_names = search_google(username)
        
        result = f"👤 **Поиск по юзернейму:** {text}\n"
        if found_names:
            result += f"📝 **Найденные имена:** {', '.join(found_names)}\n\n"
        else:
            result += "📝 **Имена:** Не найдено в открытом доступе.\n\n"
            
        result += f"🔗 **Ссылки:**\n"
        result += f"• [Telegram](https://t.me/{username})\n"
        result += f"• [VK](https://vk.com/{username})\n"
        result += f"• [Instagram](https://instagram.com/{username})\n"
        result += f"• [GitHub](https://github.com/{username})\n"
        result += f"• [TikTok](https://tiktok.com/@{username})\n"
        
        bot.reply_to(message, result, parse_mode='Markdown', disable_web_page_preview=True)
        return

    # --- ЕСЛИ ВВЕЛИ НОМЕР ---
    try:
        num = phonenumbers.parse(text, "RU")
        if not phonenumbers.is_valid_number(num):
            bot.reply_to(message, "❌ Невалидный номер или юзернейм.")
            return
            
        operator = carrier.name_for_number(num, "ru") or "Неизвестно"
        region = geocoder.description_for_number(num, "ru") or "Неизвестно"
        clean = text.replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if clean.startswith("8"): clean = "7" + clean[1:]

        found_names = search_google(text)
        
        result = f"📱 {text} | {operator} | {region}\n"
        
        if found_names:
            result += f"👤 **Найденные имена (Google):**\n"
            for name in found_names:
                result += f"• {name}\n"
        else:
            result += f"👤 **Имена:** В открытых источниках не найдено.\n"
            
        # Добавляем "плюшки" (много ссылок)
        result += (
            f"\n🔗 **Ссылки для проверки:**\n"
            f"[TG](https://t.me/+{clean}) | [WA](https://wa.me/{clean}) | "
            f"[VK](https://vk.com/search?c%5Bq%5D={clean}) | "
            f"[Авито](https://www.avito.ru/all?q={clean}) | "
            f"[Юла](https://youla.ru/search?q={clean}) | "
            f"[Google](https://www.google.com/search?q=%22{clean}%22)\n\n"
            f"💡 *Совет: если имя не найдено, попробуй поискать по ссылкам выше, там часто есть имена.*"
        )
        
        bot.reply_to(message, result, parse_mode='Markdown', disable_web_page_preview=True)
        
    except Exception as e:
        bot.reply_to(message, "⚠️ Ошибка. Введи номер в формате +7... или @username.")

if __name__ == "__main__":
    keep_alive()
    print("Бот запущен...")
    bot.polling()
