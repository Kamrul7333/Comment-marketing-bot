import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# ইউজার ডাটা এবং লিংক সেভ রাখার জন্য সাধারণ ডিকশনারি
user_links = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in user_links:
        user_links[user_id] = []

    total_links = len(user_links[user_id])
    
    text = (f"👤 *My Dashboard*\n\n"
            f"🔗 Active Links: {total_links}\n"
            f"💵 Rate: ৳1 / Member\n"
            f"💰 Balance: ৳0.00\n\n"
            f"নিচের বোতাম ব্যবহার করে আপনার ট্র্যাকিং লিংক তৈরি করুন:")

    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("➕ Create Link", callback_data="create_link"),
        InlineKeyboardButton("🔗 My Link List", callback_data="my_links"),
        InlineKeyboardButton("💸 Withdraw", callback_data="withdraw"),
        InlineKeyboardButton("🔄 Refresh", callback_data="refresh")
    )

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    user_id = call.from_user.id
    if user_id not in user_links:
        user_links[user_id] = []

    if call.data == "create_link":
        msg = bot.send_message(call.message.chat.id, "যেকোনো একটি নাম/ট্যাগ পাঠান (যেমন: Client1 বা Campaign1):")
        bot.register_next_step_handler(msg, process_link_creation)
    
    elif call.data == "my_links":
        links = user_links[user_id]
        if not links:
            bot.answer_callback_query(call.id, "আপনার কোনো সক্রিয় লিংক নেই!", show_alert=True)
        else:
            res = "🔗 *Your Generated Links:*\n\n"
            for item in links:
                res += f"📌 *{item['name']}*: {item['link']}\n"
            bot.send_message(call.message.chat.id, res, parse_mode="Markdown")

    elif call.data == "withdraw":
        bot.answer_callback_query(call.id, "উইথড্র করার মতো পর্যাপ্ত ব্যালেন্স নেই (সর্বনিম্ন ৳৫০)।", show_alert=True)

    elif call.data == "refresh":
        bot.answer_callback_query(call.id, "ড্যাশবোর্ড রিফ্রেশ করা হয়েছে!")

def process_link_creation(message):
    user_id = message.from_user.id
    link_name = message.text.strip()
    
    # এখানে আপনার চ্যানেল আইডি বা ইউজারের ইনপুট থেকে লিংক তৈরি করার ডেমো
    fake_link = f"https://t.me/your_channel?startapp={link_name}_{user_id}"
    
    user_links[user_id].append({"name": link_name, "link": fake_link})
    
    bot.reply_to(message, f"✅ *Link Created Successfully!*\n\n📌 Tag: `{link_name}`\n🔗 Link: {fake_link}", parse_mode="Markdown")

print("Bot is running...")
bot.infinity_polling()

