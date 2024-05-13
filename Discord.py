import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
from PIL import Image
import os
import time

discord_token = "Import Token Here"

load_dotenv()
client = commands.Bot(command_prefix="*", intents=discord.Intents.all())

directory = os.getcwd()
print(directory)

def split_image(image_file):
    with Image.open(image_file) as im:
        # Get the width and height of the original image
        width, height = im.size
        # Calculate the middle points along the horizontal and vertical axes
        mid_x = width // 2
        mid_y = height // 2
        # Split the image into four equal parts
        top_left = im.crop((0, 0, mid_x, mid_y))
        top_right = im.crop((mid_x, 0, width, mid_y))
        bottom_left = im.crop((0, mid_y, mid_x, height))
        bottom_right = im.crop((mid_x, mid_y, width, height))

        return top_left, top_right, bottom_left, bottom_right

async def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        # Define the output folder path
        output_folder = "output"
        # Check if the output folder exists, and create it if necessary
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_file_path = os.path.join(output_folder, filename)
        with open(output_file_path, "wb") as f:
            f.write(response.content)
        print(f"Image downloaded with original size: {filename}")

@client.event
async def on_ready():
    print("Đã Kết Nối Tới Máy Chủ DisCord")
    await client.change_presence(status=discord.Status.invisible)  # Use client instead of bot

@client.event
async def on_message(message):
    for attachment in message.attachments:
        if "Upscaled by" in message.content:
            file_prefix = 'UPSCALED_'
        else:
            file_prefix = ''
        if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            await download_image(attachment.url, f"{file_prefix}{attachment.filename}")
    # Xóa tin nhắn gần nhất sau khi tải xong hình ảnh

    # await delete_last_message(message.channel)
# time.sleep(15)
async def delete_last_message(channel):
    async for message in channel.history(limit=10):
        await message.delete()
client.run(discord_token)