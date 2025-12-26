import logging
import requests
import base64
import os
import time

import telebot
from config import TELEGRAM_BOT_TOKEN, REVE_API_KEY

logging.basicConfig(level=logging.INFO)

# ================== Reve API ==================

class ReveAPI:
    def __init__(self, api_key):
        self.URL = "https://api.reve.com/v1/"
        self.HEADERS = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def generate_image(self, prompt: str) -> dict:
        payload = {
            "prompt": prompt,
            "aspect_ratio": "16:9",
            "version": "latest"
        }

        response = requests.post(
            self.URL + "image/create",
            headers=self.HEADERS,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()

    def save_image(self, base64_string: str, file_path: str):
        decoded_data = base64.b64decode(base64_string)
        with open(file_path, "wb") as f:
            f.write(decoded_data)

# ================== BOT ==================

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
reve_api = ReveAPI(REVE_API_KEY)

# ================== HANDLERS ==================

@bot.message_handler(commands=["start", "help"])
def start_help(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет!\n\n"
        "🤖 Я бот для генерации изображений.\n"
        "✍️ Просто отправь мне текст — я превращу его в картинку.\n\n"
        "Пример:\n"
        "`Космический кот в скафандре`",
        parse_mode="Markdown"
    )

@bot.message_handler(content_types=["text"])
def generate_image_handler(message):
    # Сообщение о генерации
    status_message = bot.send_message(
        message.chat.id,
        "🎨 Генерирую картинку..."
    )

    # Эффект печати
    bot.send_chat_action(message.chat.id, "typing")

    try:
        result = reve_api.generate_image(message.text)

        if "image" not in result:
            bot.send_message(
                message.chat.id,
                "❌ API не вернул изображение."
            )
            return

        image_path = "result.png"
        reve_api.save_image(result["image"], image_path)

        with open(image_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo)

        # Удаляем сообщение "Генерирую..."
        bot.delete_message(
            message.chat.id,
            status_message.message_id
        )

        # Удаляем файл с компьютера
        os.remove(image_path)

    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"⚠️ Ошибка: {e}"
        )

# ================== START ==================

if __name__ == "__main__":
    print("🤖 Бот запущен")
    bot.infinity_polling()
