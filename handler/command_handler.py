import os 
from discord.ext import commands 

async def load_all(bot: commands.Bot):
  except_files = ['utils.py']
  for category in os.listdir(os.path.join(os.getcwd(), 'commands')):
    for command in os.listdir(os.path.join(os.getcwd(), 'commands', category)):
      if command.endswith('.py') and command not in except_files:
        await bot.load_extension(f'commands.{category}.{command[:-3]}')
      
  print('All command loaded!')
