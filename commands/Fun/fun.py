from io import BytesIO
import os
from typing import Optional 
import dotenv
import discord 
from discord.ext import commands 
from PIL import Image
from discord import app_commands 


dotenv.load_dotenv()

class Fun(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    
  @app_commands.command(name='wanted', description='Membuat gambar wanted user')
  async def wanted(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
    if user is None:
      user_profile = interaction.user.display_avatar.with_size(128)
    else:
      user_profile = user.display_avatar.with_size(128)
    await interaction.response.send_message('tunggu sebentar...')
    wanted_img = Image.open(os.path.join(os.getcwd(), 'commands', 'Fun', 'assets', 'wanted.jpg')) 
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
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Fun(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])