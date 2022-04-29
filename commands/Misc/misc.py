from io import BytesIO
import os
import random
from re import A
from typing import Optional
import dotenv
import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from discord import app_commands
from commands.utils import generate_time


dotenv.load_dotenv()

class Misc(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.fonts = os.path.join(os.getcwd(), 'fonts')


  @commands.command(name='totext', description='Convert isi file yang kamu kirim ke text')
  async def totext(self, ctx: commands.Context):
    if len(ctx.message.attachments) == 0:
      return await ctx.reply('Tolong tautkan file!')
    file = ctx.message.attachments[0]
    text = await file.read()
    text = text.decode()
    await ctx.reply(f'```{file.url[-2:]}{text}```')


async def setup(bot: commands.Bot):
  await bot.add_cog(Misc(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])