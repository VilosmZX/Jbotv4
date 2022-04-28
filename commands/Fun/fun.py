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

class Fun(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    
    
  @app_commands.command(name='wanted', description='Membuat gambar wanted user')
  async def wanted(self, interaction: discord.Interaction, user: Optional[discord.Member] = None, price: Optional[int] = None):
    if user is None:
      user_profile = interaction.user.display_avatar.with_size(128)
    else:
      user_profile = user.display_avatar.with_size(128)
    
    await interaction.response.send_message('tunggu sebentar...')
    wanted_img = Image.open(os.path.join(os.getcwd(), 'commands', 'Fun', 'assets', 'wanted.jpg')) 
    font = ImageFont.truetype('fonts/ibm/IBMPlexSans-Bold.ttf', 24)
    draw = ImageDraw.Draw(wanted_img)
    if price is not None:
      text = 'Rp' + str(price)
    elif price is None:
      text = 'Rp' + '1000000'
      
    draw.text((60, 613), text, (0, 0, 0), font)
    data = BytesIO(await user_profile.read())
    pfp = Image.open(data)
    pfp = pfp.resize((376, 376))
    wanted_img.paste(pfp, (55, 192))
    wanted_img.save(os.path.join(os.getcwd(), 'commands', 'Fun', 'saved', f'wanted_{interaction.user.id}.jpg'))
    await interaction.edit_original_message(attachments=[discord.File(os.path.join(os.getcwd(), 'commands', 'Fun', 'saved', f'wanted_{interaction.user.id}.jpg'))])
    
    
  @app_commands.command(name='trigger', description='Trigger user with image')
  async def trigger(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
    if user is None:
      user_profile = interaction.user.display_avatar.with_size(128)
    else:
      user_profile = user.display_avatar.with_size(128)
    await interaction.response.send_message('tunggu sebentar...')
    trigger_img = Image.open(os.path.join(os.getcwd(), 'commands', 'Fun', 'assets', 'triggered.jpg'))
    pfp = Image.open(BytesIO(await user_profile.read()))
    pfp = pfp.resize((96, 73))
    trigger_img.paste(pfp, (76, 78))
    trigger_img.save(os.path.join(os.getcwd(), 'commands', 'Fun', 'saved', f'triggered_{interaction.user.id}.jpg'))
    await interaction.edit_original_message(attachments=[discord.File(os.path.join(os.getcwd(), 'commands', 'Fun', 'saved', f'triggered_{interaction.user.id}.jpg'))])

  

  @app_commands.command(name='gay', description='Mengukur tingkat gay seseorang')
  async def gay(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
    if user is None:
      user = interaction.user 
    percentage = random.randint(1, 101)
    embed = discord.Embed()
    if percentage <= 50:
      embed.color = discord.Color.green()
      embed.description = f'{user} {percentage}% gay, aman cuk.'
    else:
      embed.color = discord.Color.red()
      embed.description = f'{user} {percentage}% gay, hati hati cuk!!!'
    timestamp = generate_time()
    embed.set_footer(text=f'Hari ini jam {timestamp}')   
    await interaction.response.send_message(embed=embed) 
    
  @app_commands.command(name='harem', description='Menjadikan user harem')
  async def harem(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
    if user is None:
      user = interaction.user 
    await interaction.response.send_message('tunggu sebentar...')
    harem_img = Image.open(os.path.join(os.getcwd(), 'commands', 'Fun', 'assets', 'harem.jpg'))
    pfp = Image.open(BytesIO(await user.display_avatar.with_size(128).read()))
    pfp = pfp.resize((110, 115))
    pfp = pfp.rotate(-45)
    harem_img.paste(pfp, (820, 84))
    harem_img.save(os.path.join(os.getcwd(), 'commands', 'Fun', 'saved', f'harem_{interaction.user.id}.jpg'))
    await interaction.edit_original_message(attachments=[discord.File(os.path.join(os.getcwd(), 'commands', 'Fun', 'saved', f'harem_{interaction.user.id}.jpg'))])
    
  
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Fun(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])