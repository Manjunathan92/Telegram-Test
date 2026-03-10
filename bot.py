from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

TOKEN = "8577366883:AAFr5ezWqhuYl3dFiCPdynoNZKvsX8sQRX0"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

active_users = set()
user_gender = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("💬 New Anonymous Chat!", callback_data="new_chat")],
        [
            InlineKeyboardButton("👀 Browse People", callback_data="browse"),
            InlineKeyboardButton("📍 Nearby People", callback_data="nearby")
        ],
        [
            InlineKeyboardButton("🪙 Coins", callback_data="coins"),
            InlineKeyboardButton("👤 Profile", callback_data="profile"),
            InlineKeyboardButton("❓ Help", callback_data="help")
        ],
        [InlineKeyboardButton("✨ Refer to Friends (Free Coin)", callback_data="refer")],
        [InlineKeyboardButton("🔗 My Anonymous Link", callback_data="link")]
    ]

    await update.message.reply_text(
        "👋 Welcome to *HelloStrangerBot*\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    data = query.data

    if data == "new_chat":

        keyboard = [[
            InlineKeyboardButton("👨 Male", callback_data="gender_male"),
            InlineKeyboardButton("👩 Female", callback_data="gender_female")
        ]]

        await query.edit_message_text(
            "Select the gender you want to chat with:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "gender_male":

        user_gender[user_id] = "Male"

        keyboard = [
            [InlineKeyboardButton("▶ Start Chat", callback_data="start_chat")],
            [InlineKeyboardButton("❌ Cancel", callback_data="end_chat")]
        ]

        await query.edit_message_text(
            "You selected: 👨 Male\n\nPress Start Chat.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "gender_female":

        user_gender[user_id] = "Female"

        keyboard = [
            [InlineKeyboardButton("▶ Start Chat", callback_data="start_chat")],
            [InlineKeyboardButton("❌ Cancel", callback_data="end_chat")]
        ]

        await query.edit_message_text(
            "You selected: 👩 Female\n\nPress Start Chat.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "start_chat":

        gender = user_gender.get(user_id, "any")

        active_users.add(user_id)

        keyboard = [
            [InlineKeyboardButton("⏭ Next Stranger", callback_data="next")],
            [InlineKeyboardButton("❌ End Chat", callback_data="end_chat")]
        ]

        await query.edit_message_text(
            f"🔎 Searching for a {gender} stranger...",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "next":
        await query.edit_message_text("🔄 Finding another stranger...")

    elif data == "end_chat":
        active_users.discard(user_id)
        await query.edit_message_text("❌ Chat ended.")

    elif data == "browse":
        await query.edit_message_text("👀 Browse people feature coming soon.")

    elif data == "nearby":
        await query.edit_message_text("📍 Nearby people feature coming soon.")

    elif data == "coins":
        await query.edit_message_text("🪙 Your coin balance: 0")

    elif data == "profile":
        await query.edit_message_text("👤 Profile feature coming soon.")

    elif data == "help":
        await query.edit_message_text("❓ Help section coming soon.")

    elif data == "refer":
        await query.edit_message_text("✨ Invite friends and earn free coins!")

    elif data == "link":
        await query.edit_message_text("🔗 Your anonymous link will appear here.")


async def error_handler(update, context):
    print(f"Error occurred: {context.error}")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_error_handler(error_handler)

print("Bot is running...")

app.run_polling(drop_pending_updates=True)

# TOKEN = "8577366883:AAFr5ezWqhuYl3dFiCPdynoNZKvsX8sQRX0"


