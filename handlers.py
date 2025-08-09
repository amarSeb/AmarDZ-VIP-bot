# handlers.py

import telebot
from telebot import types
import config
import utils

bot = telebot.TeleBot(config.BOT_TOKEN)
pending_users = {}  # {user_id: message_id}

@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    bot.send_message(message.chat.id, "اختر من القائمة 👇", reply_markup=utils.main_menu())

@bot.message_handler(func=lambda m: m.text == "💳 الدفع والاشتراك")
def send_payment(message):
    text, kb = utils.payment_methods()
    bot.send_message(message.chat.id, text, reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "💰 الأسعار")
def send_prices(message):
    bot.send_message(message.chat.id, f"💳 سعر الاشتراك: {config.SUBSCRIPTION_PRICE_USD} أو {config.SUBSCRIPTION_PRICE_DZD}")

@bot.message_handler(func=lambda m: m.text == "📚 كورس المبتدئين")
def send_course(message):
    bot.send_message(message.chat.id, "📚 رابط كورس المبتدئين سيتم إرساله لك بعد الاشتراك.")

@bot.message_handler(func=lambda m: m.text == "🧠 القوانين")
def send_rules(message):
    bot.send_message(message.chat.id, "🧠 القوانين: يمنع نشر الروابط أو السب، والاحترام واجب.")

@bot.message_handler(func=lambda m: m.text == "👤 التواصل مع الدعم")
def send_support(message):
    bot.send_message(message.chat.id, f"📩 تواصل مع المدير: tg://user?id={config.ADMIN_ID}")

@bot.callback_query_handler(func=lambda call: call.data == "send_proof")
def ask_payment_proof(call):
    bot.send_message(call.message.chat.id, "📸 أرسل صورة أو لقطة شاشة لإثبات الدفع هنا:")
    bot.register_next_step_handler(call.message, receive_payment_proof)

def receive_payment_proof(message):
    if message.photo or message.document:
        pending_users[message.chat.id] = True

        approve_kb = types.InlineKeyboardMarkup()
        approve_kb.add(types.InlineKeyboardButton("✅ موافقة", callback_data=f"approve_{message.chat.id}"))

        bot.forward_message(config.ADMIN_ID, message.chat.id, message.message_id)
        bot.send_message(config.ADMIN_ID, f"📩 طلب جديد من @{message.from_user.username or message.from_user.first_name}\nاضغط للموافقة:", reply_markup=approve_kb)
        bot.send_message(message.chat.id, "✅ تم إرسال إثبات الدفع، في انتظار الموافقة.")
    else:
        bot.send_message(message.chat.id, "❌ يرجى إرسال صورة أو ملف فقط.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_"))
def approve_user(call):
    user_id = int(call.data.split("_")[1])
    if pending_users.get(user_id):
        bot.send_message(user_id, f"✅ تم تأكيد الدفع! انضم إلى قناتنا الخاصة:\n{config.CHANNEL_INVITE_LINK}")
        bot.send_message(call.message.chat.id, "✅ تم إرسال رابط القناة للعميل.")
        del pending_users[user_id]
    else:
        bot.send_message(call.message.chat.id, "❌ لم أجد هذا المستخدم في قائمة الانتظار.")
      
