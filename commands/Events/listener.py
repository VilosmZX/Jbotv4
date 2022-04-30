import asyncio
import datetime
import os
import dotenv
import discord
import random
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from discord import app_commands
from commands.utils.timestamp import generate_time
from commands.utils import to_circle
from io import BytesIO

dotenv.load_dotenv()
class EventListener(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.assets = os.path.join(os.getcwd(), 'commands', 'Events', 'assets')
    self.fonts = os.path.join(os.getcwd(), 'fonts', 'poppins')


  @commands.Cog.listener(name = 'on_member_join')
  async def on_member_join(self, member: discord.Member):
    welcome_channel = member.guild.get_channel(969950059401728010)
    pfp = to_circle(Image.open(BytesIO(await member.display_avatar.with_size(128).read())).convert('RGBA'), (287, 287))
    background_img = Image.open(self.assets + '/welcome.jpeg').convert('RGBA')
    font = ImageFont.truetype(self.fonts + '/Poppins-Bold.ttf', 59)
    name_font = ImageFont.truetype(self.fonts + '/Poppins-Bold.ttf', 40)
    subfont = ImageFont.truetype(self.fonts + '/Poppins-Bold.ttf', 50)
    username = f'@{member.name[:10]}...#{member.discriminator}' if len(member.name) > 10 else f'@{member}'
    draw = ImageDraw.Draw(background_img)
    draw.text((365, 13), 'WELCOME', (255, 255, 255), font, align='center')
    draw.text((376-30-(len(username) + 30), 399), f'{username}', (255, 255, 255), name_font)
    draw.text((23, 195), f'+{member.guild.member_count}', (255, 255, 255), subfont)
    background_img.paste(pfp, (368, 97), pfp)
    with BytesIO() as a:
      background_img.save(a, 'PNG')
      a.seek(0)
      await welcome_channel.send(file=discord.File(a, f'welcome_{member.name}.png'))

  @commands.Cog.listener(name='on_member_remove')
  async def on_member_remove(self, member: discord.Member):
    welcome_channel = member.guild.get_channel(969950157913333791)
    pfp = to_circle(Image.open(BytesIO(await member.display_avatar.with_size(128).read())).convert('RGBA'), (287, 287))
    background_img = Image.open(self.assets + '/welcome.jpeg').convert('RGBA')
    font = ImageFont.truetype(self.fonts + '/Poppins-Bold.ttf', 59)
    name_font = ImageFont.truetype(self.fonts + '/Poppins-Bold.ttf', 40)
    subfont = ImageFont.truetype(self.fonts + '/Poppins-Bold.ttf', 50)
    username = f'@{member.name[:10]}...#{member.discriminator}' if len(member.name) > 10 else f'@{member}'
    draw = ImageDraw.Draw(background_img)
    draw.text((370, 13), 'BYE NOB', (255, 255, 255), font, align='center')
    draw.text((376 - 30 - (len(username) + 30), 399), f'{username}', (255, 255, 255), name_font)
    draw.text((23, 195), f'-{member.guild.member_count}', (255, 255, 255), subfont)
    background_img.paste(pfp, (368, 97), pfp)
    with BytesIO() as a:
      background_img.save(a, 'PNG')
      a.seek(0)
      await welcome_channel.send(file=discord.File(a, f'welcome_{member.name}.png'))

async def setup(bot: commands.Bot):
  await bot.add_cog(EventListener(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])