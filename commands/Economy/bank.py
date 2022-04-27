from typing import Optional, Union
import os 
import dotenv
import discord 
from discord.ext import commands 
from discord import app_commands
from .utils import check_user

dotenv.load_dotenv()

class Economy(commands.Cog, app_commands.Group, name='bank'):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    self.embed = discord.Embed()
    super().__init__()
  
  @app_commands.command(name='deposit', description='Deposit semua uang mu')
  @app_commands.describe(money = 'Deposit dengan jumlah uang tertentu')
  async def deposit(self, interaction: discord.Interaction, money: Optional[int] = None):
    self.embed.clear_fields()
    self.embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
    await interaction.response.defer()
    await check_user(self.bot, interaction.user.id)
    user_data = await self.bot.collection.find_one({'_id': interaction.user.id})
    if money is None:
      if user_data['money'] <= 0:
        self.embed.color = discord.Colour.red()
        self.embed.description = '❌ Uang mu 0'
        return await interaction.followup.send(embed=self.embed)
      self.embed.description = f'✅ Berhasil mengdeposit 💰 {user_data["money"]}'
      self.embed.color = discord.Colour.green()
      user_data['bank'] += user_data['money']
      user_data['money'] = 0
      await self.bot.collection.replace_one({'_id': interaction.user.id}, user_data)
      return await interaction.followup.send(embed=self.embed)
    if money > user_data['money']:
      self.embed.description = f'❌ Uang mu kurang dari {money}'
    else:
      self.embed.description = f'✅ Berhasil mengdeposit 💰 {money}'
    self.embed.color = discord.Colour.green()
    user_data['bank'] += money 
    user_data['money'] -= money
    await self.bot.collection.replace_one({'_id': interaction.user.id}, user_data)
    return await interaction.followup.send(embed=self.embed)
  
  @app_commands.command(name = 'view', description='Melihat rekening dan uang mu')
  async def view(self, interaction: discord.Interaction):
    await check_user(self.bot, interaction.user.id)
    user_data = await self.bot.collection.find_one({'_id': interaction.user.id})
    await interaction.response.defer()
    self.embed.description = '💸 View Networth'
    self.embed.color = discord.Colour.green()
    self.embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
    self.embed.add_field(name='💰 Uang', value=user_data['money'], inline=False)
    self.embed.add_field(name='🏦 Bank', value=user_data['bank'], inline=False)
    await interaction.followup.send(embed=self.embed)
    
     
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Economy(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])