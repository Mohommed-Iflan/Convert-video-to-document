import os
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import FSInputFile

# Use TELEGRAM_TOKEN from environment or hardcoded (for testing only)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN_HERE")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(F.video)
async def convert_video_to_document(message: types.Message):
    try:
        file_id = message.video.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path

        # Download video to temp file
        downloaded_file = await bot.download_file(file_path)
        temp_filename = f"/tmp/{message.video.file_unique_id}.mp4"
        with open(temp_filename, "wb") as f:
            f.write(downloaded_file.read())

        # Send back as document
        document = FSInputFile(temp_filename, filename="converted_video.mp4")
        await message.reply_document(document, caption="✅ Converted and sent as document.")
        os.remove(temp_filename)

    except Exception as e:
        await message.reply(f"❌ Failed to convert: {e}")

@dp.message()
async def fallback(message: types.Message):
    await message.reply("Send me a Telegram video, and I’ll reupload it as a document.")

async def main():
    print("✅ Video-to-document bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
