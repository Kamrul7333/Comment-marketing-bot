import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    active_members = 0
    rate = 1
    balance = 0.00

    text = (f"👤 *My Dashboard*\n\n"
            f"👥 Active Members: {active_members}\n"
            f"💵 Rate: ৳{rate} / Member\n"
            f"💰 Available Balance: ৳{balance}")

    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("➕ Create Link", callback_data="create_link"),
        InlineKeyboardButton("🔗 My Link List", callback_data="my_links"),
        InlineKeyboardButton("🗑 Delete Link", callback_data="delete_link"),
        InlineKeyboardButton("💸 Withdraw", callback_data="withdraw"),
        InlineKeyboardButton("👤 My Account", callback_data="my_account"),
        InlineKeyboardButton("🔄 Refresh", callback_data="refresh")
    )

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

print("বট চালু হয়েছে...")
bot.polling(none_stop=True)

