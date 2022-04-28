from typing import Optional, Union
import os
from urllib import response 
import dotenv
import discord 
from discord.ext import commands 
from discord import app_commands
from commands.Economy.utils import check_user

dotenv.load_dotenv()

class Shop(commands.Cog, app_commands.Group, name='shop'):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    super().__init__()
  
  @app_commands.command(name='buy', description='Membeli barang')
  async def buy(self, interaction: discord.Interaction):
    pass 
  
  @app_commands.command(name='sell', description='Menjual barang yang kamu punya')
  async def sell(self, interaction: discord.Interaction):
    pass
    
     
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Shop(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])