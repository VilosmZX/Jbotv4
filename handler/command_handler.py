import os 
from discord.ext import commands 

async def load_all(bot: commands.Bot):
  except_files = ['utils.py', '__init__.py', 'timestamp.py', 'checkwarncollection.py']
  for category in os.listdir(os.path.join(os.getcwd(), 'commands')):
    for command in os.listdir(os.path.join(os.getcwd(), 'commands', category)):
      if command.endswith('.py') and command not in except_files:
        await bot.load_extension(f'commands.{category}.{command[:-3]}')
      
  print('All command loaded!')

async def reload_all(bot: commands.Bot):
  except_files = ['utils.py', '__init__.py', 'timestamp.py']
  for category in os.listdir(os.path.join(os.getcwd(), 'commands')):
    for command in os.listdir(os.path.join(os.getcwd(), 'commands', category)):
      if command.endswith('.py') and command not in except_files:
        await bot.reload_extension(f'commands.{category}.{command[:-3]}')
        
  print('All command reloaded!')