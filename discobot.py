import discord
from discord.ext import commands, tasks
import pytz
from datetime import datetime, timedelta
import os
from keepalive import keep_alive

# Bot token (replace with your bot token)
BOT_TOKEN = os.environ.get('token')

# Channel IDs where messages should be cleared
TARGET_CHANNEL_IDS = [1251398618087292941, 1251398909956460596]

# Nepal timezone
NEPAL_TIMEZONE = pytz.timezone('Asia/Kathmandu')

# Time to clear messages (in 24-hour format)
CLEAR_HOUR = 6
CLEAR_MINUTE = 00

class MessageClearer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.clear_messages.cancel()

    @tasks.loop(minutes=1)
    async def clear_messages(self):
        now = nepal_time_now()
        clear_time = get_clear_time()
        print(f"[DEBUG] Current time: {now}, Clear time: {clear_time}")

        if now.hour == clear_time.hour and now.minute == clear_time.minute:
            print("[DEBUG] Time to clear messages")
            for channel_id in TARGET_CHANNEL_IDS:
                channel = self.bot.get_channel(channel_id)
                if channel:
                    await clear_channel(channel)
                else:
                    print(f"Channel with ID {channel_id} not found.")

    @commands.Cog.listener()
    async def on_ready(self):
        print("[DEBUG] Bot is ready")
        if not self.clear_messages.is_running():
            self.clear_messages.start()
            print("[DEBUG] Started clear_messages task")

async def clear_channel(channel):
    clear_time = get_clear_time()
    print(f"[DEBUG] Clearing messages older than: {clear_time} in channel: {channel.name}")

    try:
        async for message in channel.history(limit=None):
            print(f"[DEBUG] Checking message from {message.created_at}")
            if message.created_at < clear_time:
                await message.delete()
                print(f"Deleted message from {channel.name} (ID: {message.id})")
    except discord.HTTPException as e:
        print(f"Failed to delete message (ID: {message.id}): {e}")

def get_clear_time():
    """Calculates the daily clearing time in Nepal time zone."""
    now = datetime.now(tz=NEPAL_TIMEZONE)
    clear_time = datetime(now.year, now.month, now.day, CLEAR_HOUR, CLEAR_MINUTE, 0, 0, tzinfo=NEPAL_TIMEZONE)
    return clear_time

def nepal_time_now():
    """Gets the current time in Nepal time zone."""
    return datetime.now(tz=NEPAL_TIMEZONE)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True  # Ensure message content intent is enabled
bot = commands.Bot(command_prefix='!', intents=intents)

# Load the cog
async def main():
    await bot.add_cog(MessageClearer(bot))
    await bot.start(BOT_TOKEN)

# Run the bot
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    keep_aive()
