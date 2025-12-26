import telebot
from logic import reve_api
from config import TOKEN

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Обработчик стартового сообщения
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет! Напиши, какую картинку ты хочешь создать, и я сделаю её для тебя."
    )

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    prompt = message.text

    # Имя файла для сохранения картинки
    image_path = f"generated_image_{message.chat.id}.png"

    # Вызываем ReveAPI для генерации изображения
    result = reve_api.generate_image(
        prompt,
        save_json=None,
        save_image=image_path     # путь к файлу с картинкой
    )

    # Проверяем возможное нарушение контентной политики
    if result.get("content_violation"):
        bot.send_message(
            message.chat.id,
            "Reve refused to generate this image because of content policy."
        )
        return

    # Отправляем изображение пользователю
    with open(image_path, "rb") as photo:
        bot.send_photo(message.chat.id, photo)

# Запуск бота
bot.polling()