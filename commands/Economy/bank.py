from typing import Optional, Union
import os
from urllib import response 
import dotenv
import discord 
from discord.ext import commands 
from discord import app_commands
from .utils import check_user
from commands.utils import generate_time

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
    self.embed.clear_fields()
    await check_user(self.bot, interaction.user.id)
    user_data = await self.bot.collection.find_one({'_id': interaction.user.id})
    await interaction.response.defer()
    self.embed.description = '💸 View Networth'
    self.embed.color = discord.Colour.green()
    self.embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
    self.embed.add_field(name='💰 Uang', value=user_data['money'], inline=False)
    self.embed.add_field(name='🏦 Bank', value=user_data['bank'], inline=False)
    await interaction.followup.send(embed=self.embed)
    
  @app_commands.command(name='withdraw', description='Ambil uang dari bank')
  async def withdraw(self, interaction: discord.Interaction, money: Optional[int] = None):
    embed = discord.Embed()
    await check_user(self.bot, interaction.user.id)
    user_data = await self.bot.collection.find_one({'_id': interaction.user.id})
    if money is None:
      embed.description = f'Berhasil Mengambil uang sebanyak {user_data["bank"]} dari bank'
      user_data['money'] += user_data['bank']
      user_data['bank'] = 0
      embed.color = discord.Color.green()
      await self.bot.collection.replace_one({'_id': interaction.user.id}, user_data)
      return await interaction.response.send_message(embed=embed)
    
    if money <= 0:
      return await interaction.response.send_message(f'Nomor tidak valid', ephemeral=True)
    if money > user_data['bank']:
      return await interaction.response.send_message(f'Uang kamu di ban kurang dari {money} rupiah.', ephemeral=True)
    user_data['money'] += money 
    user_data['bank'] -= money 
    embed.description = f'Berhasil Mengambil uang sebanyak {money} dari bank'
    embed.color = discord.Color.blue()
    await self.bot.collection.replace_one({'_id': interaction.user.id}, user_data)
    return await interaction.response.send_message(embed=embed)
  
  
  @app_commands.command(name='transfer', description='Transfer uang ke bank orang lain')
  @app_commands.describe(user = 'User yang ingin kamu transfer', money = 'Jumlah Uang yang ingin kamu transfer')
  async def transfer(self, interaction: discord.Interaction, user: discord.Member, money: int):
    embed = discord.Embed()
    await check_user(self.bot, interaction.user.id)
    await check_user(self.bot, user.id)
    minimum_money = 50000
    your_data = await self.bot.collection.find_one({'_id': interaction.user.id})
    user_data = await self.bot.collection.find_one({'_id': user.id})
    if money < minimum_money:
      embed.description = f'Jumlah Minimum 💰 {money}'
      return await interaction.response.send_message(embed=embed, ephemeral=True)
    if money > your_data['bank']:
      embed.description = f'Uang di bank kurang dari 💰 {money}'
      return await interaction.response.send_message(embed=embed, ephemeral=True)
    embed.description = f'✅ Transfer berhasil!\n\nDari: {interaction.user.mention}\nKepada: {user.mention}\nJumlah: Rp.{money}\n'
    user_data['bank'] += money 
    your_data['bank'] -= money 
    embed.description += f'Sisa: Rp.{your_data["bank"]}\n''\n'
    embed.set_author(name=user, icon_url=user.display_avatar.url)
    timestamp = generate_time()
    embed.set_footer(text=f'Hari ini, jam {timestamp}')
    await interaction.response.send_message(embed=embed)
    
    
  
  


    
     
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Economy(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])