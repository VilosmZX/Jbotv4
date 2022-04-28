from datetime import datetime
import os
from typing import Optional 
import dotenv
import discord 
from discord.ext import commands 
from discord import app_commands
from commands.utils import generate_time

dotenv.load_dotenv()

class Admin(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    
  class Confirm(discord.ui.View):
    def __init__(self, user: discord.Member):
      super().__init__()
      self.value = None 
      self.user = user
      
      
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.primary)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
      await interaction.response.send_message(f'Confirming', ephemeral=True)
      self.value = True 
      self.stop()
      
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
      await interaction.response.send_message('Cancelling', ephemeral=True)
      self.value = False 
      self.stop()
    
    
  @app_commands.command(name='kick', description='Kick user dari server')
  @app_commands.checks.has_permissions(kick_members=True)
  async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: Optional[str] = 'Tanpa Alasan'):
    
    if user.guild_permissions.administrator:
      return await interaction.response.send_message('Kamu gak bisa kick seorang administrator.', ephemeral=True)
    view = self.Confirm(user)
    await interaction.response.send_message(f'Kick {user} karena {reason}?', view=view, ephemeral=True)
    await view.wait()
    if view.value:
      embed = discord.Embed()
      embed.description = f'Hello {user.mention},\n\nKamu telah di kick dari server {interaction.guild.name}'
      embed.set_thumbnail(url=interaction.guild.icon.url)
      embed.set_footer(text=f'di kick oleh {interaction.user} karena {reason}\n\nJika ada kesalahan silahkan hubungi {interaction.user}')
      await user.send(embed=embed)
      await user.kick(reason=reason)
      
  @app_commands.command(name='ban', description='Ban user dari server')
  @app_commands.checks.has_permissions(ban_members=True)
  async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: Optional[str] = 'Tanpa Alasan'):
    
    if user.guild_permissions.administrator:
      return await interaction.response.send_message('Kamu gak bisa ban seorang administrator.', ephemeral=True)
    view = self.Confirm(user)
    await interaction.response.send_message(f'Ban {user} karena {reason}?', view=view, ephemeral=True)
    await view.wait()
    if view.value:
      embed = discord.Embed()
      embed.description = f'Hello {user.mention},\n\nKamu telah di ban dari server {interaction.guild.name}'
      embed.set_thumbnail(url=interaction.guild.icon.url)
      embed.set_footer(text=f'di ban oleh {interaction.user} karena {reason}\n\nJika ada kesalahan silahkan hubungi {interaction.user}')
      await user.send(embed=embed)
      await user.ban(reason=reason)
      
  @app_commands.command(name='clearbans', description='Mengunban semua user yang telah di ban')
  @app_commands.checks.has_permissions(ban_members=True)
  async def clearbans(self, interaction: discord.Interaction, reason: Optional[str] = None):
    embed = discord.Embed()
    timestamp = generate_time()
    embed.description = f'Tidak ada user yang terkena ban'
    embed.set_footer(text=f'hari ini jam {datetime.now().strftime("%H:%M")}')
    if len([user async for user in interaction.guild.bans()]) == 0:
      return await interaction.response.send_message(embed=embed, ephemeral=True)
    total_user = 0
    async for entry in interaction.guild.bans():
      total_user += 1
      await interaction.guild.unban(entry.user, reason=reason)
    embed = discord.Embed()
    embed.description = f'{total_user} user berhasil di unban!'
    embed.set_footer(text=f'hari ini jam {timestamp}')
    await interaction.response.send_message(embed=embed, ephemeral=True)
      
      
  @kick.error 
  @ban.error
  async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
      return await interaction.response.send_message('Tidak ada akses.', ephemeral=True)
    elif isinstance(error, app_commands.TransformerError):
       return await interaction.response.send_message('User tidak ditemukan', ephemeral=True)
      
    
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Admin(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])