# =========================================
# FREE FIRE TOPUP BOT FINAL FIXED
# =========================================

# INSTALL:
# pip install pyTelegramBotAPI

import telebot
import sqlite3
from telebot.types import *

# =========================================
# SETTINGS
# =========================================

TOKEN = "8665154268:AAF1AMzAjvUwKO7kpo5jWjmQUvbwsikExxM"
ADMIN_ID = 7263633862
UPI_ID = "armaan-hacks@fam"

bot = telebot.TeleBot(TOKEN)

# =========================================
# DATABASE
# =========================================

conn = sqlite3.connect("ff_bot.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    uid TEXT,
    package TEXT,
    amount INTEGER,
    status TEXT
)
""")

conn.commit()

# =========================================
# START
# =========================================

@bot.message_handler(commands=['start'])
def start(message):

    cursor = conn.cursor()

    user_id = message.chat.id

    cursor.execute(
        "INSERT OR IGNORE INTO users(user_id,balance) VALUES(?,?)",
        (user_id,0)
    )

    conn.commit()

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("💎 Buy Diamonds")
    markup.row("💰 Balance", "💳 Add Balance")
    markup.row("📦 My Orders", "🆔 My ID")

    bot.send_message(
        message.chat.id,
        "🔥 FREE FIRE TOPUP BOT 🔥",
        reply_markup=markup
    )

# =========================================
# MY ID
# =========================================

@bot.message_handler(func=lambda m: m.text == "🆔 My ID")
def myid(message):

    bot.send_message(
        message.chat.id,
        f"🆔 Your ID: {message.chat.id}"
    )

# =========================================
# BALANCE
# =========================================

@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def balance(message):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM users WHERE user_id=?",
        (message.chat.id,)
    )

    data = cursor.fetchone()

    if data:
        bal = data[0]
    else:
        bal = 0

    bot.send_message(
        message.chat.id,
        f"💰 Balance: ₹{bal}"
    )

# =========================================
# ADD BALANCE
# =========================================

@bot.message_handler(func=lambda m: m.text == "💳 Add Balance")
def add_balance(message):

    text = f"""
💳 ADD BALANCE

💰 UPI ID:
{UPI_ID}

📸 Send Payment Screenshot After Payment
"""

    bot.send_message(
        message.chat.id,
        text
    )

    try:
        bot.send_photo(
            message.chat.id,
            open("qr.jpg", "rb")
        )
    except:
        pass

# =========================================
# SCREENSHOT
# =========================================

@bot.message_handler(content_types=['photo'])
def photo(message):

    caption = f"""
💰 NEW PAYMENT

👤 User ID: {message.chat.id}
👤 Name: {message.from_user.first_name}
"""

    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            "✅ Add ₹100",
            callback_data=f"add100|{message.chat.id}"
        )
    )

    markup.add(
        InlineKeyboardButton(
            "✅ Add ₹500",
            callback_data=f"add500|{message.chat.id}"
        )
    )

    bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=caption,
        reply_markup=markup
    )

    bot.send_message(
        message.chat.id,
        "✅ Screenshot Sent To Admin"
    )

# =========================================
# BUY DIAMONDS
# =========================================

@bot.message_handler(func=lambda m: m.text == "💎 Buy Diamonds")
def buy(message):

    msg = bot.send_message(
        message.chat.id,
        "🎮 Send Free Fire UID:"
    )

    bot.register_next_step_handler(msg, get_uid)

def get_uid(message):

    uid = message.text

    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            "💎 100 Diamonds - ₹80",
            callback_data=f"buy|{uid}|100|80"
        )
    )

    markup.add(
        InlineKeyboardButton(
            "💎 310 Diamonds - ₹240",
            callback_data=f"buy|{uid}|310|240"
        )
    )

    markup.add(
        InlineKeyboardButton(
            "💎 520 Diamonds - ₹400",
            callback_data=f"buy|{uid}|520|400"
        )
    )

    bot.send_message(
        message.chat.id,
        "✅ Select Package",
        reply_markup=markup
    )

# =========================================
# CALLBACKS
# =========================================

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    cursor = conn.cursor()

    data = call.data.split("|")

    # =====================================
    # ADD 100
    # =====================================

    if data[0] == "add100":

        user_id = int(data[1])

        cursor.execute(
            "SELECT balance FROM users WHERE user_id=?",
            (user_id,)
        )

        bal = cursor.fetchone()[0]

        new_bal = bal + 100

        cursor.execute(
            "UPDATE users SET balance=? WHERE user_id=?",
            (new_bal,user_id)
        )

        conn.commit()

        bot.send_message(
            user_id,
            "✅ ₹100 Added"
        )

        bot.answer_callback_query(
            call.id,
            "Success"
        )

    # =====================================
    # ADD 500
    # =====================================

    elif data[0] == "add500":

        user_id = int(data[1])

        cursor.execute(
            "SELECT balance FROM users WHERE user_id=?",
            (user_id,)
        )

        bal = cursor.fetchone()[0]

        new_bal = bal + 500

        cursor.execute(
            "UPDATE users SET balance=? WHERE user_id=?",
            (new_bal,user_id)
        )

        conn.commit()

        bot.send_message(
            user_id,
            "✅ ₹500 Added"
        )

        bot.answer_callback_query(
            call.id,
            "Success"
        )

    # =====================================
    # BUY
    # =====================================

    elif data[0] == "buy":

        uid = data[1]
        package = data[2]
        amount = int(data[3])

        cursor.execute(
            "SELECT balance FROM users WHERE user_id=?",
            (call.message.chat.id,)
        )

        bal = cursor.fetchone()[0]

        if bal < amount:

            bot.send_message(
                call.message.chat.id,
                "❌ Low Balance"
            )

            return

        new_bal = bal - amount

        cursor.execute(
            "UPDATE users SET balance=? WHERE user_id=?",
            (new_bal,call.message.chat.id)
        )

        cursor.execute("""
        INSERT INTO orders(user_id,uid,package,amount,status)
        VALUES(?,?,?,?,?)
        """,
        (
            call.message.chat.id,
            uid,
            package,
            amount,
            "Pending"
        ))

        conn.commit()

        order_id = cursor.lastrowid

        bot.send_message(
            call.message.chat.id,
            f"""
✅ ORDER PLACED

🆔 Order ID: {order_id}
🎮 UID: {uid}
💎 Diamonds: {package}
💰 Amount: ₹{amount}

⏳ Status: Pending
"""
        )

        markup = InlineKeyboardMarkup()

        markup.add(
            InlineKeyboardButton(
                "✅ Complete Order",
                callback_data=f"complete|{order_id}"
            )
        )

        bot.send_message(
            ADMIN_ID,
            f"""
🔥 NEW ORDER

🆔 Order ID: {order_id}
👤 User: {call.message.chat.id}
🎮 UID: {uid}
💎 Package: {package}
💰 Amount: ₹{amount}
""",
            reply_markup=markup
        )

    # =====================================
    # COMPLETE ORDER
    # =====================================

    elif data[0] == "complete":

        order_id = int(data[1])

        cursor.execute(
            "UPDATE orders SET status=? WHERE id=?",
            ("Completed",order_id)
        )

        conn.commit()

        cursor.execute(
            "SELECT user_id FROM orders WHERE id=?",
            (order_id,)
        )

        user_id = cursor.fetchone()[0]

        bot.send_message(
            user_id,
            f"✅ Order #{order_id} Completed"
        )

        bot.answer_callback_query(
            call.id,
            "Order Completed"
        )

# =========================================
# MY ORDERS
# =========================================

@bot.message_handler(func=lambda m: m.text == "📦 My Orders")
def orders(message):

    cursor = conn.cursor()

    cursor.execute("""
    SELECT id,package,status
    FROM orders
    WHERE user_id=?
    ORDER BY id DESC
    LIMIT 10
    """,
    (message.chat.id,)
    )

    data = cursor.fetchall()

    if not data:

        bot.send_message(
            message.chat.id,
            "❌ No Orders"
        )

        return

    text = "📦 YOUR ORDERS\n\n"

    for i in data:

        text += f"""
🆔 #{i[0]}
💎 {i[1]}
📌 {i[2]}

"""

    bot.send_message(
        message.chat.id,
        text
    )

# =========================================
# ADMIN ADD BALANCE
# =========================================

@bot.message_handler(commands=['addbal'])
def addbal(message):

    if message.chat.id != ADMIN_ID:
        return

    try:

        cursor = conn.cursor()

        cmd = message.text.split()

        user_id = int(cmd[1])
        amount = int(cmd[2])

        cursor.execute(
            "SELECT balance FROM users WHERE user_id=?",
            (user_id,)
        )

        bal = cursor.fetchone()[0]

        new_bal = bal + amount

        cursor.execute(
            "UPDATE users SET balance=? WHERE user_id=?",
            (new_bal,user_id)
        )

        conn.commit()

        bot.send_message(
            message.chat.id,
            "✅ Balance Added"
        )

        bot.send_message(
            user_id,
            f"💰 ₹{amount} Added"
        )

    except:

        bot.send_message(
            message.chat.id,
            "Use:\n/addbal userid amount"
        )

# =========================================
# RUN
# =========================================

print("BOT RUNNING...")

bot.infinity_polling()