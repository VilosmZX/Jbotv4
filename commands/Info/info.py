from io import BytesIO
import os
from PIL import Image, ImageDraw, ImageFont, ImageChops
from typing import Optional
import discord 
from discord.ext import commands 
from discord import app_commands
from commands.Economy.utils import check_user

class Information(commands.Cog, app_commands.Group, name='info'):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    super().__init__()
    
  def circle(self, pfp: Image.Image, size=(215, 215)):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert('RGBA')
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0)+bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp
    
  @app_commands.command(name='user', description='Melihat info tentang user')
  @app_commands.describe(user = 'Melihat info user, kosongkan untuk melihat info diri sendiri')
  async def user(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
    await interaction.response.defer()
    assets_folder = os.path.join(os.getcwd(), 'commands', 'Info', 'assets')
    if user is None:
      user = interaction.user 
    await check_user(self.bot, user.id)
    name, nickname, user_id, status = str(user), user.display_name, user.id, str(user.status).upper()
    created_at = user.created_at.strftime('%a %b\n%B %Y') 
    joined_at = user.created_at.strftime('%a %b\n%B %Y')
    money, level = (await self.bot.collection.find_one({'_id': user.id}))['money'], 'COMINGSOON'
    base_img = Image.open(assets_folder + '/base.png').convert('RGBA')
    banner = Image.open(assets_folder + '/animebg.png').convert('RGBA')
    pfp = user.display_avatar.with_size(128)
    pfp = Image.open(BytesIO(await pfp.read())).convert('RGBA')
    name = f'{name[:16]}..' if len(name) > 16 else name 
    nickname = f'AKA - {nickname[:16]}..' if len(nickname) > 16 else f'AKA - {nickname}'
    draw = ImageDraw.Draw(base_img)
    pfp = self.circle(pfp)
    font = ImageFont.truetype('fonts/nunito/static/Nunito-Regular.ttf', 38)
    akafont = ImageFont.truetype('fonts/nunito/static/Nunito-Regular.ttf', 30)
    subfont = ImageFont.truetype('fonts/nunito/static/Nunito-Regular.ttf', 25)
    draw.text((280, 240), name, font=font)
    draw.text((270, 315), nickname, font=akafont)
    draw.text((65, 490), str(user_id), font=subfont)
    draw.text((405, 490), status, font=subfont)
    draw.text((65, 635), str(money), font=subfont)
    draw.text((405, 635), level, font=subfont)
    draw.text((65, 770), created_at, font=subfont)
    draw.text((405, 770), joined_at, font=subfont)
    base_img.paste(pfp, (56, 158), pfp)
    
    banner.paste(base_img, (0, 0), base_img)
    
    with BytesIO() as a:
      banner.save(a, 'PNG')
      a.seek(0)
      
      await interaction.followup.send(file=discord.File(a, 'profile.png'))
    

    
  
  
async def setup(bot: commands.Bot):
  await bot.add_cog(Information(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])  
