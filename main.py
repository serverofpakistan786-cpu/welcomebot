import os
import asyncio
from datetime import timedelta
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ChatPermissions
)
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_USERNAME = "PMOZIX"

WELCOME_DELETE_TIME = 30  # seconds

WELCOME_TEXT = """
━━━━━━━━━━━━━━━━━━━━━━
        W E L C O M E
━━━━━━━━━━━━━━━━━━━━━━

H E Y   {first_name}
A A P K A   I S   G R O U P   M E
D I L   S E   S W A G A T   H A I

━━━━━━━━━━━━━━━━━━━━━━
N A M E        :   {first_name}
U S E R N A M E :   @{username}
━━━━━━━━━━━━━━━━━━━━━━

R E S P E C T   E V E R Y O N E
N O   S P A M
S T A Y   A C T I V E

━━━━━━━━━━━━━━━━━━━━━━
G R O U P   O W N E R
P M   O Z I X
━━━━━━━━━━━━━━━━━━━━━━
"""

RULES_TEXT = """
━━━━━━━━━━━━━━━━━━━━━━
        G R O U P   R U L E S
━━━━━━━━━━━━━━━━━━━━━━

1. R E S P E C T   E V E R Y O N E
2. N O   S P A M
3. N O   A B U S E
4. O N L Y   R E L E V A N T   C H A T
5. A D M I N   D E C I S I O N   F I N A L

━━━━━━━━━━━━━━━━━━━━━━
👑 G R O U P   O W N E R
P M   O Z I X
━━━━━━━━━━━━━━━━━━━━━━
"""

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        first_name = member.first_name.upper()
        username = member.username.upper() if member.username else "NOT AVAILABLE"

        text = WELCOME_TEXT.format(
            first_name=first_name,
            username=username
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "C O N T A C T   O W N E R",
                url=f"https://t.me/{OWNER_USERNAME}"
            )]
        ])

        with open("welcome.jpg", "rb") as img:
            msg = await update.message.reply_photo(
                photo=img,
                caption=text,
                reply_markup=keyboard
            )

        await msg.react("🔥")
        await asyncio.sleep(WELCOME_DELETE_TIME)
        await msg.delete()

async def owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👑 G R O U P   O W N E R : P M   O Z I X\nhttps://t.me/{OWNER_USERNAME}"
    )

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(RULES_TEXT)

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("REPLY TO USER TO MUTE")

    admin = await update.effective_chat.get_member(update.effective_user.id)
    if admin.status not in ["administrator", "creator"]:
        return await update.message.reply_text("ONLY ADMINS CAN USE THIS")

    user_id = update.message.reply_to_message.from_user.id
    await update.effective_chat.restrict_member(
        user_id,
        ChatPermissions(can_send_messages=False),
        until_date=timedelta(minutes=10)
    )
    await update.message.reply_text("USER MUTED FOR 10 MINUTES")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("REPLY TO USER TO BAN")

    admin = await update.effective_chat.get_member(update.effective_user.id)
    if admin.status not in ["administrator", "creator"]:
        return await update.message.reply_text("ONLY ADMINS CAN USE THIS")

    user_id = update.message.reply_to_message.from_user.id
    await update.effective_chat.ban_member(user_id)
    await update.message.reply_text("USER BANNED")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(CommandHandler("owner", owner))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("ban", ban))

    print("BOT RUNNING...")
    app.run_polling()

if __name__ == "__main__":
    main()
