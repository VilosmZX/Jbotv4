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

class General(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.fonts = os.path.join(os.getcwd(), 'fonts')


  @app_commands.command(name='amiadmin', description='Check apakah kamu admin atau tidak')
  async def amiadmin(self, interaction: discord.Interaction):
    is_admin = None
    for role in interaction.user.roles:
      if role.permissions.ban_members or role.permissions.administrator:
        is_admin = True

    embed = discord.Embed(color=discord.Color.random())
    if is_admin:
      embed.description = f'{interaction.user.mention} adalah seorang admin!'
      return await interaction.response.send_message(embed=embed)
    embed.description = f'{interaction.user.mention} bukan seorang admin!'
    return await interaction.response.send_message(embed=embed)


  @app_commands.command(name = 'avatar', description='Mendapatkan gambar dari avatar mu')
  async def avatar(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
    if user is None:
      user = interaction.user
    avatar = Image.open(BytesIO(await user.display_avatar.with_size(256).read()))
    with BytesIO() as a:
      avatar.save(a, 'PNG')
      a.seek(0)
      await interaction.response.send_message(file=discord.File(a, f'avatar_{user.id}.png'))

  @app_commands.command(name = 'report', description='Report user')
  async def report(self, interaction: discord.Interaction, user: discord.Member, reason: str):
    report_channel = await interaction.guild.fetch_channel(970293995018276965)
    embed = discord.Embed(description=f'Report dari {interaction.user.mention}\nSuspect: {user.mention}\n\nAlasan Lebih Lengkap:\n{reason}')
    embed.set_footer(text=f'Report masuk jam {generate_time()}')
    await interaction.response.send_message(f'Report telah di record, admin akan segera memeriksa nya.', ephemeral=True)
    await report_channel.send(embed=embed)










async def setup(bot: commands.Bot):
  await bot.add_cog(General(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])