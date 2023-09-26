import asyncio
import telegram
import sys

sys.stdout.reconfigure(encoding="utf-8") # Some characters in news are not compatible with 'unicode'
token="" # Replace the token you got from BotFather
bot = telegram.Bot(token)
group_id = 0 #Replace the group or person id here

async def send_message(text):
    async with bot:
        await bot.send_message(text=text,chat_id=group_id)
        
async def main():
    async with bot:
        updates= await bot.getUpdates()
        for update in updates:
            print(update)