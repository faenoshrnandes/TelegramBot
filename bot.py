from pyrogram import Client, filters
import time
import asyncio

# Replace with your API details
API_ID = "8314131"
API_HASH = "f5648c77bb1e15c61358dd4aa945120d"
SESSION_STRING = "your_generated_session_string"

# Dictionary to track user messages
user_message_count = {}
blocked_users = {}
BLOCK_THRESHOLD = 3  # Messages before bot responds
BLOCK_DURATION = 60  # Temporary block duration in seconds

app = Client("UserBot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

@app.on_message(filters.private & ~filters.me)
def auto_reply(client, message):
    user_id = message.from_user.id
    
    # Track user message count
    if user_id not in user_message_count:
        user_message_count[user_id] = 0
    user_message_count[user_id] += 1
    
    # If user reaches message threshold, send a response
    if user_message_count[user_id] == BLOCK_THRESHOLD:
        message.reply_text("Hello There OWl BOT Here Garmin is currently unavailable at the moment. Please wait! while he gets back")
    elif user_message_count[user_id] > BLOCK_THRESHOLD:
        message.reply_text("You're sending too many messages. Temporarily blocking you!")
        client.block_user(user_id)
        blocked_users[user_id] = time.time()
        user_message_count[user_id] = 0
    
async def unblock_users():
    while True:
        current_time = time.time()
        for user_id in list(blocked_users.keys()):
            if current_time - blocked_users[user_id] >= BLOCK_DURATION:
                await app.unblock_user(user_id)
                del blocked_users[user_id]
        await asyncio.sleep(10)  # Check every 10 seconds

# Start the bot
app.start()
asyncio.run(unblock_users())
