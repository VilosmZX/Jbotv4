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

  @app_commands.command(name = 'nickname', description='Mengubah nama mu')
  async def change_nickname(self, interaction: discord.Interaction, username: str):
    embed = discord.Embed(description=f'Mengubah nama dari {interaction.user.display_name} -> {username}')
    await interaction.user.edit(nick=username)
    await interaction.response.send_message(embed=embed, ephemeral=True)




async def setup(bot: commands.Bot):
  await bot.add_cog(General(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])