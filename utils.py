# utils.py

from telebot import types
import config

def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("💳 الدفع والاشتراك", "💰 الأسعار")
    kb.add("📚 كورس المبتدئين", "🧠 القوانين")
    kb.add("👤 التواصل مع الدعم")
    return kb

def payment_methods():
    text = (
        f"طرق الدفع المتاحة:\n\n"
        f"✅ PayPal : {config.PAYPAL_EMAIL}\n"
        f"💳 سعر الاشتراك: {config.SUBSCRIPTION_PRICE_USD} مدى الحياة\n\n"
        f"✅ BaridiMob : {config.BARIDIMOB_NUMBER}\n"
        f"📱 الدفع عبر BaridiMob ({config.SUBSCRIPTION_PRICE_DZD})\n\n"
        f"✅ USDT (BEP20 - BNB Smart Chain):\n"
        f"{config.USDT_ADDRESS_1}\nأو\n{config.USDT_ADDRESS_2}\n"
    )

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ أرسـل إثبات الدفع", callback_data="send_proof"))
    return text, kb
  
