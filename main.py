import telebot
from telebot import types
import subprocess
import os
import random
import requests

bot = telebot.TeleBot('YOUR_TOKEN')
bot_owner_id = 'YOUR_TELEGRAM_ID'

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Suggest message",
                                        callback_data='suggest')
    keyboard.add(button)
    bot.send_message(
        message.chat.id,
        f"Hello, {message.from_user.first_name}! Enter your message  ",
        reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'suggest')
def suggest(call):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Ready 🚀"))
    bot.send_message(
        call.message.chat.id,
        "Great! Now you can send me any file or text. ",
        reply_markup=keyboard)
    bot.register_next_step_handler(call.message, process_suggestion)


def process_suggestion(message):
    if message.document:
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("suggestion.txt", "wb") as out_file:
            out_file.write(downloaded_file)
        if message.caption:
            with open("suggestion.txt", "a") as file:
                file.write(message.caption)
        bot.send_message(message.chat.id, "File saved successfully ")
        send_suggestion_to_owner(message.chat.id)
        subprocess.Popen(["python", "bot.py"])
        exit()
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("suggestion.jpg", "wb") as out_file:
            out_file.write(downloaded_file)
        if message.caption:
            with open("suggestion.txt", "w") as file:
                file.write(message.caption)
        else:
            with open("suggestion.txt", "w") as file:
                file.write("")
        bot.send_message(message.chat.id, "Photo saved successfully ")
        send_suggestion_to_owner(message.chat.id)
        subprocess.Popen(["python", "bot.py"])
        exit()
    elif message.video:
        file_id = message.video.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("suggestion.mp4", "wb") as out_file:
            out_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Video saved successfully!")
        send_suggestion_to_owner(message.chat.id)
        subprocess.Popen(["python", "bot.py"])
        exit()
    elif message.text:
        with open("suggestion.txt", "w") as file:
            file.write(message.text)
        bot.send_message(message.chat.id, "Thank you for your nessage!")
        send_suggestion_to_owner(message.chat.id)
        subprocess.Popen(["python", "bot.py"])
        exit()
    else:
        bot.send_message(
            message.chat.id,
            "Sorry, An error has occurred ."
        )


def send_suggestion_to_owner(chat_id):
    with open("suggestion.txt", "r") as file:
        suggestion = file.read()
    if os.path.exists("suggestion.jpg"):
        with open("suggestion.jpg", "rb") as photo:
            bot.send_photo(
                bot_owner_id,
                photo,
                caption=f'New message from {chat_id}\n\n{suggestion}',
                parse_mode='Markdown')
    else:
        bot.send_message(
            bot_owner_id,
            f'New  message{chat_id}\n\n{suggestion}',
            parse_mode='Markdown')
    os.remove("suggestion.txt")
    if os.path.exists("suggestion.jpg"):
        os.remove("suggestion.jpg")
    if os.path.exists("suggestion.mp4"):
        os.remove("suggestion.mp4")
    subprocess.Popen(["python", "bot.py"])
    exit()

bot.polling(non_stop=True, interval=0)
