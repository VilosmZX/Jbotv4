from discord.ext import commands 

async def check_user(bot: commands.Bot, id: int):
  user_data = await bot.collection.find_one({'_id': id})
  if user_data is None:
    new_data = {
      '_id': id,
      'money': 0,
      'bank': 0,
      'items': []
    }
    return await bot.collection.insert_one(new_data)
  
  