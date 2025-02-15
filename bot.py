import os
from pyrogram import Client, filters
from pyrogram.types import Message
import time
from dotenv import load_dotenv  # Load .env file

load_dotenv()  # Load environment variables

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("offline_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user_message_count = {}
warning_threshold = 2
block_duration = 300
blocked_users = {}

@app.on_message(filters.private & ~filters.bot)
def auto_reply(client: Client, message: Message):
    user_id = message.from_user.id
    current_time = time.time()
    
    if user_id in blocked_users and current_time < blocked_users[user_id]:
        return
    
    if user_id not in user_message_count:
        user_message_count[user_id] = 1
    else:
        user_message_count[user_id] += 1
    
    if user_message_count[user_id] == 1:
        message.reply_text("Please wait, my master is not available. Could you wait?")
    elif user_message_count[user_id] >= warning_threshold:
        message.reply_text("/dwarn You are sending too many messages. You are temporarily blocked.")
        blocked_users[user_id] = current_time + block_duration  
        user_message_count[user_id] = 0  

app.run()

