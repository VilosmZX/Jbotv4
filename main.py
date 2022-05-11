import asyncio
import os
import discord
from handler import load_all
from discord.ext import commands 
import dotenv
import motor.motor_asyncio as motor
from website import run
import wavelink

dotenv.load_dotenv()

class Bot(commands.Bot):
  def __init__(self):
    super().__init__(
      command_prefix='j!',
      intents=discord.Intents.all(),
      application_id=int(os.environ.get('APPID'))
    )

  async def node_connect(self):
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot=bot, host='lavalinkinc.ml', port=443, password='incognito', https=True)

  async def setup_hook(self) -> None:
      await load_all(bot)
      # Remove this to set The command globally
      await bot.tree.sync(guild=discord.Object(id=int(os.environ.get('GUID'))))

      
  async def close(self) -> None:
      return await super().close()
    
  async def on_ready(self):
    print(f'Bot is online!')
    await self.loop.create_task(self.node_connect())

bot = Bot()

async def main():
  bot.mongo = motor.AsyncIOMotorClient(os.environ.get('SRV'))
  bot.db = bot.mongo['jbot']
  bot.collection = bot.db['economy']
  bot.warns = bot.db['warn']
  await bot.start(os.environ.get('TOKEN'))
  

asyncio.run(main())
    

