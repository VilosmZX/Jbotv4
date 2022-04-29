from io import BytesIO
import os
import random
from re import A
import string
from typing import Optional 
import dotenv
import discord 
from discord.ext import commands 
from PIL import Image, ImageFont, ImageDraw, ImageChops
from discord import app_commands 
from commands.utils import generate_time
import aiohttp
from googletrans import Translator

dotenv.load_dotenv()

class Fun(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    self.assets = os.path.join(os.getcwd(), 'commands', 'Fun', 'assets')
    self.fonts = os.path.join(os.getcwd(), 'fonts')
    self.translator = Translator()
    
    
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
    with BytesIO() as a:
      wanted_img.save(a, 'PNG')
      a.seek(0)
      await interaction.edit_original_message(content='', attachments=[discord.File(a, f'wanted_image.png')])
    
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


  @app_commands.command(name = 'quotes', description='Jika kamu sedih dan putus asa silahkan jalankan command ini')
  @app_commands.choices(
    option = [
      app_commands.Choice(name = 'random', value=1),
      app_commands.Choice(name='popular', value=2),
      app_commands.Choice(name='teknologi', value=2),
      app_commands.Choice(name='sejarah', value=2),
    ]
  )
  async def quotes(self, interaction: discord.Interaction, option: int):
    url = 'https://api.quotable.io'
    embed = discord.Embed(color=discord.Color.random())
    async with aiohttp.ClientSession() as session:
      endpoint = None 
      if option == 1:
        endpoint = url + '/random'
      elif option == 2:
        endpoint = url + '/random?tags=famous-quotes'
      elif option == 3:
        endpoint = url + '/random?tags=technology'
      elif option == 4:
        endpoint = url + '/random?tags=history'
      async with await session.get(endpoint) as response:
        data = await response.json()
        text = self.translator.translate(data['content'], src='en', dest='id')
        embed.description = f'***{text.text}***'
        embed.set_footer(text=f'Quote by {data["author"]}')
        await interaction.response.send_message(embed=embed)
        
  @app_commands.command(name = 'animal', description='Idk random bet soalnya')
  @app_commands.choices(
    option = [
        app_commands.Choice(name = 'dog', value=1),
        app_commands.Choice(name = 'cat', value=2),
    ]
  )
  async def animal(self, interaction: discord.Interaction, option: int):
    await interaction.response.send_message('Mengambil data...')
    url = 'https://random-stuff-api.p.rapidapi.com/animals/'
    headers = {
      'Authorization': 'Iif8PB48eRoT',
      'X-RapidAPI-Host': 'random-stuff-api.p.rapidapi.com',
      'X-RapidAPI-Key': '8259075b20msh8ff5c35111a7496p1e5967jsn537bb2a3bc16'
    }
    async with aiohttp.ClientSession(headers=headers) as session:
      category = None 
      if option == 1:
        category = 'DOG'
      elif option == 2:
        category = 'CAT'
      async with await session.get(url + category, params={'limit': 1}) as response:
        data = await response.json()
        async with await session.get(data[0]['url']) as image:
          image = BytesIO(await image.read())
          await interaction.edit_original_message(content='Selesai.', attachments=[discord.File(image, f'{category}.png')])
          
          
  @app_commands.command(name = 'weather', description='Mendapatkan informasi cuacah')
  @app_commands.describe(query = 'Nama kota atau negara atau provinsi')
  async def weather(self, interaction: discord.Interaction, query: str):
    params = {
      'q': query.strip().replace(',', ''),
      'lang': 'id'
    }
    
    headers = {
      'X-RapidAPI-Host': 'community-open-weather-map.p.rapidapi.com',
      'X-RapidAPI-Key': '8259075b20msh8ff5c35111a7496p1e5967jsn537bb2a3bc16'
    }
    await interaction.response.send_message('Mengambil data...')
    async with aiohttp.ClientSession(headers=headers) as session:
      url = 'https://community-open-weather-map.p.rapidapi.com/weather'
      async with await session.get(url, params=params) as response:
        data = await response.json()
        embed = discord.Embed(color=discord.Color.random())
        emoji = None 
        if data['weather'][0]['main'] == 'Clouds':
          emoji = '☁'
        elif data['weather'][0]['main'] == 'Rain':
          emoji = '🌧'
        elif data['weather'][0]['main'] == 'Wind':
          emoji = '🌫'
        elif data['weather'][0]['main'] == 'Snowy':
          emoji = '🌨'
        elif data['weather'][0]['main'] == 'Sunlight':
          emoji = '⛅'
        
        embed.description = f'{emoji} {str(data["weather"][0]["description"]).upper()}'
        embed.set_footer(text=f'Di {data["name"]}')
        await interaction.edit_original_message(embed=embed)
        
        




  
  
  
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Fun(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])