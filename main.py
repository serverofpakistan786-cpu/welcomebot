from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, MessageHandler, filters

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
OWNER_USERNAME = "PMOZIX68"   # WITHOUT @

WELCOME_TEXT = """
━━━━━━━━━━━━━━━━━━━━━━
        W E L C O M E
━━━━━━━━━━━━━━━━━━━━━━

H E Y   {first_name}  
A A P K A   I S   G R O U P   M E  
D I L   S E   S W A G A T   H A I

Y E   G R O U P   B A N A   H A I  
M U S I C   L O V E R S  
A U R   E K   S A T H  
M A S T I   K A R N E  
W A L E   L O G O N   K E   L I Y E

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

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:

        first_name = member.first_name.upper()
        username = member.username.upper() if member.username else "NOT AVAILABLE"

        text = WELCOME_TEXT.format(
            first_name=first_name,
            username=username
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "C O N T A C T   O W N E R",
                    url=f"https://t.me/{OWNER_USERNAME}"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            text=text,
            reply_markup=reply_markup
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome)
    )
    print("BOT RUNNING...")
    app.run_polling()

if __name__ == "__main__":
    main()
