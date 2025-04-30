from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Namaste! Main ek story generator bot hoon.\n"
        "Aapko apni kahani banane ke liye kuch questions jawab dene padenge. Type karein: /story"
    )

async def story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Aapki kahani banane ke liye kuch sawalon ka jawab dein:")
    await update.message.reply_text("1. Aapka character ka naam kya hai?")

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    if 'character_name' not in context.chat_data:
        context.chat_data['character_name'] = user_input
        await update.message.reply_text("2. Character kis jagah par hai? (Jaise jungle, sheher, etc.)")
    elif 'place' not in context.chat_data:
        context.chat_data['place'] = user_input
        await update.message.reply_text("3. Aapka character kis challenge ka samna kar raha hai?")
    elif 'challenge' not in context.chat_data:
        context.chat_data['challenge'] = user_input
        character = context.chat_data['character_name']
        place = context.chat_data['place']
        challenge = context.chat_data['challenge']
        story = (
            f"Yeh kahani hai {character} ki, jo {place} mein tha. Ek din, usse {challenge} ka samna karna pada.\n"
            "Aapke character ka reaction kya hoga?\n"
            "1. Taqat ka istemal\n2. Doston se madad\n3. Dimaag ka istemal"
        )
        await update.message.reply_text(story)
        context.chat_data['story_phase'] = 'challenge_decision'
    elif context.chat_data.get('story_phase') == 'challenge_decision':
        character = context.chat_data['character_name']
        if user_input == "1":
            await update.message.reply_text(f"{character} ne apni taqat se challenge ka samna kiya.")
        elif user_input == "2":
            await update.message.reply_text(f"{character} ne doston se madad li aur challenge ka samna kiya.")
        elif user_input == "3":
            await update.message.reply_text(f"{character} ne dimaag se kaam liya aur challenge solve kiya.")
        else:
            await update.message.reply_text("Kripya 1, 2, ya 3 mein se ek option dein.")
            return
        await update.message.reply_text("Ab ending choose karein:\n1. Happy Ending\n2. Sad Ending")
        context.chat_data['story_phase'] = 'ending'
    elif context.chat_data.get('story_phase') == 'ending':
        character = context.chat_data['character_name']
        if user_input == "1":
            await update.message.reply_text(f"Kahani khatam hoti hai ek Happy Ending ke saath. {character} jeet gaya!")
        elif user_input == "2":
            await update.message.reply_text(f"Kahani khatam hoti hai ek Sad Ending ke saath. {character} haar gaya.")
        else:
            await update.message.reply_text("Kripya 1 ya 2 mein se ek choose karein.")
            return
        context.chat_data.clear()

BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("story", story))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))

app.run_polling()
