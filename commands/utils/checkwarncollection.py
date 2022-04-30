import discord 
from discord.ext import commands 

async def check_warn_collection(bot: commands.Bot, userID: int):
  if await bot.warns.find_one({'_id': userID}) == None:
    new_data = {
      '_id': userID,
      'total_warn': 0,
      'total_kicked': 0,
    }
    await bot.warns.insert_one(new_data)
  
    