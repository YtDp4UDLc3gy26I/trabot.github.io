from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import time
import threading

# Your bot's token (replace with your actual bot token)
TOKEN = '7283938352:AAEbRWnN17AUXQTTlkPeSHfLpUga6QLxFgI'

# Progress variable to track user progress
user_progress = {}

# Dictionary to hold auto ad watching status for users
auto_watch_status = {}

# Function to handle /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Monetag Mini App bot!\nUse /watch_ad to watch an ad, /auto_watch to start auto ads, and /stop_auto to stop them.')

# Function to simulate watching an ad
def watch_ad(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_progress:
        user_progress[user_id] = 0
    
    user_progress[user_id] += 10
    if user_progress[user_id] > 100:
        user_progress[user_id] = 100
    
    update.message.reply_text(f'You have watched an ad! Progress: {user_progress[user_id]}%')

# Function to start auto-watching ads
def auto_watch(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    
    # Check if the user already has auto-watching running
    if user_id in auto_watch_status and auto_watch_status[user_id] is True:
        update.message.reply_text('Auto ad watching is already running!')
        return
    
    # Start auto ad watching in a separate thread
    def start_auto_watch():
        while user_id in auto_watch_status and auto_watch_status[user_id]:
            time.sleep(10)
            if user_id in user_progress:
                user_progress[user_id] += 10
                if user_progress[user_id] > 100:
                    user_progress[user_id] = 100
                context.bot.send_message(chat_id=user_id, text=f'You have watched an ad! Progress: {user_progress[user_id]}%')

    auto_watch_status[user_id] = True
    threading.Thread(target=start_auto_watch).start()
    update.message.reply_text('Auto ad watching started!')

# Function to stop auto-watching ads
def stop_auto(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in auto_watch_status and auto_watch_status[user_id]:
        auto_watch_status[user_id] = False
        update.message.reply_text('Auto ad watching stopped.')
    else:
        update.message.reply_text('Auto ad watching is not active.')

# Function to handle errors
def error(update: Update, context: CallbackContext) -> None:
    print(f"Update {update} caused error {context.error}")

# Main function to run the bot
def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("watch_ad", watch_ad))
    dispatcher.add_handler(CommandHandler("auto_watch", auto_watch))
    dispatcher.add_handler(CommandHandler("stop_auto", stop_auto))

    # Log all errors
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
