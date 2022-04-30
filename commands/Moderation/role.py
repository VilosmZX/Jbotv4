import os
from typing import Optional
import dotenv
import discord 
from discord.ext import commands 
from discord import app_commands

dotenv.load_dotenv()

class Lock(commands.Cog, app_commands.Group, name = 'lock'):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    super().__init__()
    
  @app_commands.command(name = 'give', description='Memberikan role kepada user')
  @app_commands.checks.has_permissions(manage_roles=True)
  async def give_role(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role):
    embed = discord.Embed(color = discord.Color.random())
    if user.get_role(role.id) == None:
      embed.description = f'{user.mention} sudah memiliki role {role}'
      return await interaction.response.send_message(embed=embed)
    embed.description = f'Memberikan role {role} kepada {user}'
    await user.add_roles(role)
    await interaction.response.send_message(embed=embed)
      
  @give_role.error 
  async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
      if isinstance(error, app_commands.MissingPermissions):
        return await interaction.response.send_message('Tidak ada akses', ephemeral=True)
      
  @app_commands.command(name = 'remove', description='Mengambil role dari user')
  @app_commands.checks.has_permissions(manage_roles=True)
  async def remove_role(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role):
    embed = discord.Embed(color = discord.Color.random())
    if user.get_role(role.id) == None:
      embed.description = f'{user.mention} tidak memiliki role {role}'
      return await interaction.response.send_message(embed=embed)
    embed.description = f'Mengambil role {role} dari {user.mention}'
    await user.remove_roles(role)
    await interaction.response.send_message(embed=embed)
    

async def setup(bot: commands.Bot):
  await bot.add_cog(Lock(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])
  