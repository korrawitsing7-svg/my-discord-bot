from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# เรียกใช้งานระบบเปิดพอร์ตเว็บก่อนรันบอท
keep_alive()

import discord
from discord.ext import commands
import os

# ตั้งค่าบอท
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# ตัวแปรเก็บจำนวนรีวิวเริ่มต้น
review_count = 24782 

# ⚠️ ใส่ ID ห้องรีวิวของบีมตรงนี้ (วิธีเอา ID: คลิกขวาที่ชื่อห้องใน Discord -> กด Copy Channel ID)
REVIEW_CHANNEL_ID = 123456789012345678  

@bot.event
async def on_ready():
    print(f'บอท {bot.user} ออนไลน์เรียบร้อยแล้ว!')

@bot.event
async def on_message(message):
    global review_count
    
    # ข้ามข้อความจากบอทเอง
    if message.author.bot:
        return

    # เช็กว่าพิมพ์ในห้องรีวิว และมีคำว่า +1 หรือไม่
    if message.channel.id == REVIEW_CHANNEL_ID and "+1" in message.content:
        review_count += 1
        
        # สั่งเปลี่ยนชื่อห้องตามจำนวนรีวิวใหม่
        new_channel_name = f"⭐ | รีวิวยศซามู · {review_count}"
        await message.channel.edit(name=new_channel_name)
        
        # ส่งสติ๊กเกอร์/ตอบรับข้อความ
        await message.add_reaction("✅")

    await bot.process_commands(message)

# รันบอทผ่าน Token ที่ซ่อนไว้ใน Secrets
bot.run(os.environ['DISCORD_TOKEN'])
