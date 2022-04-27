import asyncio
import datetime
import os 
import dotenv
import discord 
import random
from discord.ext import commands 
from discord import app_commands
from .utils import check_user

dotenv.load_dotenv()

class Economy(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    self.embed = discord.Embed()
    
  
  @app_commands.command(name='beg', description='Meminta minta uang')
  @app_commands.checks.cooldown(1, 60)
  async def beg(self, interaction: discord.Interaction):
    await check_user(self.bot, interaction.user.id)
    await interaction.response.defer()
    self.embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
    self.embed.color = discord.Colour.green()
    money_received = random.randint(500, 5000)
    user_data = await self.bot.collection.find_one({'_id': interaction.user.id})
    user_data['money'] += money_received
    await self.bot.collection.replace_one({'_id': interaction.user.id}, user_data)
    self.embed.description = f'✅ Kamu berhasil mendapatkan uang **{money_received} rupiah** dari mengemis'
    await interaction.followup.send(embed=self.embed)
    
    
  @beg.error 
  async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
      await interaction.response.defer(ephemeral=True)
      time_remaining = datetime.timedelta(seconds=error.retry_after)
      msg = await interaction.followup.send(f'Command ini masih dalam mode coooldown, coba lagi dalam {time_remaining.seconds} detik.')
  
  
    
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Economy(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])