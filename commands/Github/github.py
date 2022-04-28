import requests
import discord 
from discord.ext import commands 
from discord import app_commands
import asyncio
import aiohttp
import os
from commands.utils import generate_time

class Github(commands.Cog, app_commands.Group, name='github'):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    super().__init__()
   
   
  @app_commands.command(name='user')
  async def user(self, interaction: discord.Interaction, username: str):
    async with aiohttp.ClientSession() as session:
      embed = discord.Embed(color=discord.Color.green(), title=username)
      url = f'https://api.github.com/users/{username}'
      async with session.get(url) as res:
        if res.status == 200:
          user_data = await res.json()
          embed.url = user_data['html_url']
          embed.set_author(name=user_data['login'], icon_url=user_data['avatar_url'])
          embed.add_field(name='Company', value=user_data['company'], inline=False)
          embed.add_field(name='Followers', value=user_data['followers'])
          embed.add_field(name='Following', value=user_data['following'], inline=False)
          embed.add_field(name='Public Repos', value=user_data['public_repos'])
          embed.add_field(name='Location', value=user_data['location'], inline=False)
          timestamp = generate_time()
          embed.set_footer(text=f'Hari ini jam {timestamp}')
        else:
          embed.clear_fields()
          embed.set_author(name='Not Found')
          timestamp = generate_time()
          embed.set_footer(text=f'Hari ini jam {timestamp}')
          return await interaction.response.send_message(embed=embed)
      return await interaction.response.send_message(embed=embed)
    
  # @app_commands.command(name='orgs')
  # async def orgs(self, interaction: discord.Interaction, organization: str):
  #   async with aiohttp.ClientSession() as session:
  #     embed = discord.Embed(color=discord.Color.green())
  #     url = f'https://api.github.com/orgs/{organization}/repos'
  #     async with session.get(url) as res:
  #       if res.status == 200:
  #         orgs_data = await res.json()
          
  #       else:
  #         embed.clear_fields()
  #         embed.set_author(name='Not Found')
  #         timestamp = generate_time()
  #         embed.set_footer(text=f'Hari ini jam {timestamp}')
  #         return await interaction.response.send_message(embed=embed)
          
          
     


async def setup(bot: commands.Bot):
  await bot.add_cog(Github(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])