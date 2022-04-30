from io import BytesIO
import os
from PIL import Image, ImageDraw, ImageFont, ImageChops
from typing import Optional, Tuple
import discord 
from discord.ext import commands 
from discord import app_commands
from commands.Economy.utils import check_user

class Information(commands.Cog, app_commands.Group, name='info'):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    super().__init__()
    self.assets = os.path.join(os.getcwd(), 'commands', 'Info', 'assets')
    self.fonts = os.path.join(os.getcwd(), 'fonts')

  def convert_to_circle(self, pfp: Image.Image, size: Tuple[int, int]) -> Image.Image:
    pfp = pfp.resize(size, Image.ANTIALIAS)
    mask = Image.new('L', pfp.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + pfp.size, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    pfp.putalpha(mask)
    return pfp


  @app_commands.command(name = 'user', description='Melihat info tentang user')
  async def userinfo(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
    if user is None:
      user  = interaction.user
    await check_user(self.bot, user.id)
    await interaction.response.defer()
    base_img = Image.open(self.assets + '/profile.png').convert('RGBA')
    pfp = Image.open(BytesIO(await user.display_avatar.with_size(128).read())).convert('RGBA')
    username = f'@{str(user.name)[0:16]}..#{user.discriminator}' if len(str(user)) > 16 else f'@{user}'
    userID = str(user.id)
    status = str(user.status).upper()
    money = (await self.bot.collection.find_one({'_id': user.id}))
    networth = str(money['money'] + money['bank'])
    roles = ''.join(f'@{role}\n' for role in user.roles).replace('@@everyone\n', '')
    font = ImageFont.truetype(self.fonts + '/nunito/static/Nunito-Regular.ttf', 50)
    rolefont = ImageFont.truetype(self.fonts + '/nunito/static/Nunito-Light.ttf', 30)
    pfp = self.convert_to_circle(pfp, (197, 203))
    draw = ImageDraw.Draw(base_img)
    base_img.paste(pfp, (42, 52), pfp)
    draw.text((449, 124), f'Rp{networth}', font=font)
    draw.text((449, 271), username, font=font)
    draw.text((449, 411), userID, font=font)
    draw.text((449, 576), status, font=font)
    draw.text((38, 389), roles, font=rolefont, fill=(255, 255, 255))
    with BytesIO() as a:
      base_img.save(a, 'PNG')
      a.seek(0)
      await interaction.followup.send(file=discord.File(a, f'{username}.png'))
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Information(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])  
