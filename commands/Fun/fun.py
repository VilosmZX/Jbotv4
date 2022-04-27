import os 
import dotenv
import discord 
from discord.ext import commands 

dotenv.load_dotenv()

class Fun(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Fun(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])