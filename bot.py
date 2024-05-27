import os
import ssl
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pytube import YouTube
from pydub import AudioSegment
import certifi

# Ensure you have the latest certificates
os.environ['SSL_CERT_FILE'] = certifi.where()

# Bypass SSL verification (use this only if the certifi solution doesn't work)
ssl._create_default_https_context = ssl._create_unverified_context

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token
BOT_TOKEN = '7048298713:AAH38dAIJEbsZnFWMoxu86NLZvmKydgqJIM'

# Welcome message
WELCOME_MESSAGE = "Hello! ကျနော် Tashido ပါ။ mp3 ပြောင်းဖို့ /start ကို နှိပ်ပါခင်ဗျာ"
START_MESSAGE = "Hello! ကျနော် Tashido ပါ။ ကျနော့်ကို youtube link လေးပေးပါခင်ဗျာ"
CONVERT_ANOTHER = "နောက်ထပ်ပြောင်းဖို့ /start ကိုနှိပ်ပါခင်ဗျာ"
INVALID_LINK = "Link လေးမှားယွင်းနေပါတယ်ခင်ဗျာ၊ သေချာပြန်ယူပေးကြည့်ပါ"

# Define start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(START_MESSAGE)

# Define message handler for YouTube links
def handle_message(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    if message_text.startswith('https://www.youtube.com/') or message_text.startswith('https://youtu.be/'):
        update.message.reply_text("Downloading and converting the video. Please wait...")
        try:
            # Download and convert video to mp3
            video = YouTube(message_text)
            audio_stream = video.streams.filter(only_audio=True).first()
            output_file = audio_stream.download(output_path='downloads/')
            base, ext = os.path.splitext(output_file)
            mp3_file = base + '.mp3'
            AudioSegment.from_file(output_file).export(mp3_file, format='mp3')
            os.remove(output_file)
            
            # Send the mp3 file to the user
            update.message.reply_audio(audio=open(mp3_file, 'rb'))
            os.remove(mp3_file)
            update.message.reply_text(CONVERT_ANOTHER)
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            update.message.reply_text(f"An error occurred: {e}")
    else:
        update.message.reply_text(INVALID_LINK)

# Main function to start the bot
def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
