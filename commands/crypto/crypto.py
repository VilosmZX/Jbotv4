import discord
from discord.ext import commands 
from discord import app_commands 
import os
import web3



class Crypto(commands.Cog, app_commands.Group, name = 'crypto'):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    super().__init__()

  @app_commands.command(name = 'fromweitoeth', description='Convert wei to eth')
  async def fromweitoeth(self, interaction: discord.Interaction, wei: int):
    eth = web3.Web3.fromWei(wei, 'ether')
    await interaction.response.send_message(f'Eth: {eth:f}')
    
  @app_commands.command(name = 'fromethtowei', description='Convert eth to wei')
  async def fromethtowei(self, interaction: discord.Interaction, eth: float):
    wei = eth * (10 ** 18)
    await interaction.response.send_message(f'Wei: {wei:f}')
    


async def setup(bot: commands.Bot):
  await bot.add_cog(Crypto(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])


