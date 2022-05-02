import os
from typing import Optional
import dotenv
import discord 
from discord.ext import commands 
from discord import app_commands

dotenv.load_dotenv()

class Role(commands.Cog, app_commands.Group, name = 'role'):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    super().__init__()
    
  @app_commands.command(name = 'give', description='Memberikan role kepada user')
  @app_commands.checks.has_permissions(manage_roles=True)
  async def give_role(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role):
    await interaction.response.defer()
    embed = discord.Embed(color = discord.Color.random())
    if user.guild_permissions.administrator:
      return await interaction.response.send_message(f'{user} adalah seorang administrator')
    if user.get_role(role.id) != None:
      embed.description = f'{user.mention} sudah memiliki role {role}'
      return await interaction.followup.send(embed=embed)
    embed.description = f'Memberikan role {role} kepada {user}'
    await user.add_roles(role)
    await interaction.followup.send(embed=embed)
      
      
  @app_commands.command(name = 'remove', description='Mengambil role dari user')
  @app_commands.checks.has_permissions(manage_roles=True)
  async def remove_role(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role):
    embed = discord.Embed(color = discord.Color.random())
    if user.guild_permissions.administrator:
      return await interaction.response.send_message(f'{user} adalah seorang administrator')
    if user.get_role(role.id) == None:
      embed.description = f'{user.mention} tidak memiliki role {role}'
      return await interaction.response.send_message(embed=embed)
    embed.description = f'Mengambil role {role} dari {user.mention}'
    await user.remove_roles(role)
    await interaction.response.send_message(embed=embed)
  
  
  @app_commands.command(name = 'new', description='Add new role')
  @app_commands.checks.has_permissions(manage_roles = True)
  @app_commands.choices(
    mentionable = [
      app_commands.Choice(name = 'yes', value=1),
      app_commands.Choice(name = 'no', value=2),
    ],
  )
  @app_commands.describe(name = 'Nama role', display_icon = 'Icon dari role Harus serve boost', mentionable='bisa dimention orang atau ga, Default nya True')
  async def new_role(self, interaction: discord.Interaction, name: str, display_icon: str = None, mentionable: int = True):
    if mentionable == 1:
      mentionable = True 
    elif mentionable == 2:
      mentionable = False 
      
    role = await interaction.channel.guild.create_role(name = name, permissions=discord.Permissions.general(), color=discord.Color.random(), display_icon=display_icon, mentionable=mentionable)
    await interaction.response.send_message(f'Berhasil menambahkan role {role.mention}')

  @app_commands.command(name = 'delete', description='Delete role dari server')
  @app_commands.checks.has_permissions(manage_roles=True)
  async def delete_role(self, interaction: discord.Interaction, role: discord.Role):
    await interaction.response.defer()
    embed = discord.Embed(color = discord.Color.random())
    embed.description = f'Role {role.mention} berhasil di delete'
    await interaction.followup.send(embed=embed)
    await interaction.guild.get_role(role.id).delete()



  @give_role.error
  @remove_role.error
  @new_role.error
  async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
      if isinstance(error, app_commands.MissingPermissions):
        return await interaction.response.send_message('Tidak ada akses', ephemeral=True)
      
  
    
  

async def setup(bot: commands.Bot):
  await bot.add_cog(Role(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])
  