from io import BytesIO
import os
import random
from re import A
from typing import Optional 
import dotenv
import discord 
from discord.ext import commands 
from PIL import Image, ImageFont, ImageDraw, ImageChops
from discord import app_commands 
from commands.utils import generate_time


dotenv.load_dotenv()

class Fun(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    self.assets = os.path.join(os.getcwd(), 'commands', 'Fun', 'assets')
    self.fonts = os.path.join(os.getcwd(), 'fonts')
    
    
  @app_commands.command(name='wanted', description='Membuat gambar wanted user')
  async def wanted(self, interaction: discord.Interaction, user: Optional[discord.Member] = None, price: Optional[int] = None):
    if user is None:
      user_profile = interaction.user.display_avatar.with_size(128)
    else:
      user_profile = user.display_avatar.with_size(128)
    
    await interaction.response.send_message('tunggu sebentar...')
    wanted_img = Image.open(os.path.join(os.getcwd(), 'commands', 'Fun', 'assets', 'wanted.jpg'), Image.ANTIALIAS)
    font = ImageFont.truetype('fonts/ibm/IBMPlexSans-Bold.ttf', 24)
    draw = ImageDraw.Draw(wanted_img)
    if price is not None:
      text = 'Rp' + str(price)
    elif price is None:
      text = 'Rp' + '1000000'
      
    draw.text((60, 613), text, (0, 0, 0), font)
    data = BytesIO(await user_profile.read())
    pfp = Image.open(data, Image.ANTIALIAS)
    pfp = pfp.resize((376, 376))
    wanted_img.paste(pfp, (55, 192))
    with BytesIO() as a:
      wanted_img.save(a, 'PNG')
      a.seek(0)
      await interaction.edit_original_message(content='', attachments=[discord.File(a, f'wanted_{user.name}.png')])
    
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
    with BytesIO() as a:
      trigger_img.save(a, 'PNG')
      a.seek(0)
      await interaction.edit_original_message(content='', attachments=[discord.File(a, f'triggered{user.name}.png')])
  

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
    with BytesIO() as a:
      harem_img.save(a, 'PNG')
      a.seek(0)
      await interaction.edit_original_message(content='', attachments=[discord.File(a, f'harem{user.name}.png')])

  @app_commands.command(name='marry', description='nikahkan dua orang dengan template muka jes dan derren omg!!!')
  async def marry(self, interaction: discord.Interaction, first_user: discord.Member, second_user: discord.Member):
    await interaction.response.defer()
    msg = await interaction.followup.send('tunggu sebentar.')
    jesder_img = Image.open(self.assets + '/derjes.jpeg')
    first_user_pfp = Image.open(BytesIO(await first_user.display_avatar.with_size(128).read())).resize((112, 113), Image.ANTIALIAS)
    second_user_pfp = Image.open(BytesIO(await second_user.display_avatar.with_size(128).read())).resize((125, 112), Image.ANTIALIAS)
    draw = ImageDraw.Draw(jesder_img)
    font = ImageFont.truetype(self.fonts + '/nunito/static/Nunito-Black.ttf', 30)
    draw.text((56, 346), f'@{str(first_user)}', (0, 0, 0), font)
    draw.text((480, 413), f'@{str(second_user)}', (0, 0, 0), font)
    jesder_img.paste(first_user_pfp, (34, 188))
    jesder_img.paste(second_user_pfp, (514, 213))
    with BytesIO() as a:
      jesder_img.save(a, 'PNG')
      a.seek(0)
      await interaction.edit_original_message(content=f'Omg selamat {first_user.mention} dan {second_user.mention} karena sudah menikah semoga cepet punya anak OMG!!!', attachments=[discord.File(a, f'{first_user}_{second_user}.png')])
      
  @app_commands.command(name='wut', description='Wut???')
  async def wut(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
    if user is None:
      user = interaction.user 
    await interaction.response.defer()
    msg = await interaction.followup.send('tunggu sebentar.')
    wut_img = Image.open(self.assets + '/what.png').convert('RGBA')
    wut_img = wut_img.resize((round(wut_img.size[0] * 0.5), round(wut_img.size[1] * 0.5)))
    pfp = Image.open(BytesIO(await user.display_avatar.with_size(128).read())).convert('RGBA')
    pfp = pfp.resize((round(429 * 0.5), round(382 * 0.5)))
    wut_img.paste(pfp, (round(425 * 0.5), round(219 * 0.5)))
    with BytesIO() as a:
      wut_img.save(a, 'PNG')
      a.seek(0)
      await interaction.edit_original_message(content=f'', attachments=[discord.File(a, f'wut.png')])

  def circle(self, pfp: Image.Image, size: tuple):
    pfp = pfp.resize(size, Image.ANTIALIAS)
    mask = Image.new('L', pfp.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + pfp.size, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

  @app_commands.command(name = 'berlyn', description='Berlyn love gishel')
  async def berlyn(self, interaction: discord.Interaction, user: Optional[discord.Member] = None, pesan: Optional[str] = 'Berlyn sangat cinta gishel'):
    await interaction.response.send_message('tunggu sebentar')
    if user is None:
      user = interaction.user
    berlyn_img = Image.open(self.assets + '/berlyn.png').convert('RGBA')
    pfp = Image.open(BytesIO(await user.display_avatar.with_size(128).read())).convert('RGBA')
    pfp = self.circle(pfp, (306, 422))
    berlyn_img.paste(pfp, (104, 242),pfp)
    font = ImageFont.truetype(self.fonts + '/nunito/static/Nunito-Regular.ttf', 35)
    subfont = ImageFont.truetype(self.fonts + '/nunito/static/Nunito-Light.ttf', 20)
    draw = ImageDraw.Draw(berlyn_img)
    draw.text((25, 820), str(user), font=font, fill=(0, 0, 0))
    draw.text((25, 860), str(pesan), font=subfont, fill=(0, 0, 0))
    with BytesIO() as a:
      berlyn_img.save(a, 'PNG')
      a.seek(0)
      await interaction.edit_original_message(content='Selesai.', attachments=[discord.File(a, 'a.png')])





  
  
  
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Fun(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])