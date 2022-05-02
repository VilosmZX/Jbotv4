from datetime import datetime
import os
from shutil import move
from typing import Optional 
import dotenv
import discord 
from discord.ext import commands 
from discord import app_commands
from commands.utils import generate_time
from commands.utils import check_warn_collection
import random
from asyncio.exceptions import TimeoutError

dotenv.load_dotenv()

class Admin(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    self.exception_channel = [969590898260312064, 969786263957807104]
    
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
    
  @app_commands.command(name = 'lockdown', description='Lockdown semua channel')
  @app_commands.choices(
    option = [
      app_commands.Choice(name = 'on', value=1),
      app_commands.Choice(name = 'off', value=2)
    ]
  )
  @app_commands.checks.has_permissions(manage_channels=True)
  async def lockdown(self, interaction: discord.Interaction, option: int):
    await interaction.response.defer()
    everyone_role = interaction.guild.get_role(756105841429708830)
    total_text_channel = 0
    total_voice_channel = 0
    status = None 
    for channel in await interaction.guild.fetch_channels():
      c: discord.abc.GuildChannel = channel
      perm = None 
      if option == 1:
        perm = False 
        status = 'lock'
      else:
        perm = True 
        status = 'unlock'
      if c.type == discord.ChannelType.text and c.id not in self.exception_channel:
        await c.set_permissions(everyone_role, send_messages=perm)
        total_text_channel += 1
      elif c.type == discord.ChannelType.voice and c.id not in self.exception_channel:
        await c.set_permissions(everyone_role, connect=perm)
        total_voice_channel += 1
    embed = discord.Embed(title='⚠ Lockdown')
    embed.description = f'\n{total_text_channel} text channel di {status} 🔒\n{total_voice_channel} voice channel di {status} 🔒'
    await interaction.followup.send(embed=embed)


  @app_commands.command(name = 'clear', description='Clear semua message dari channel')
  @app_commands.checks.has_permissions(manage_messages=True)
  @app_commands.describe(channel = 'nama channel yang ingin clear message nya')
  async def clear(self, interaction: discord.Interaction, channel: Optional[discord.TextChannel] = None):
    if channel is None:
      channel: discord.TextChannel = interaction.channel
    await channel.purge()
    await interaction.response.send_message(f'semua pesan berhasil dihapus', ephemeral=True)

  @app_commands.command(name = 'setnickname', description='Mengubah nickname dari user')
  @app_commands.checks.has_permissions(manage_nicknames=True)
  @app_commands.describe(user = 'User yang ingin diganti nama nya', nickname = 'Nama user yang baru')
  async def setnickname(self, interaction: discord.Interaction, user: discord.Member, nickname: str):
    embed = discord.Embed(description=f'Mengubah nama dari {user.display_name} -> {nickname}')
    await user.edit(nick=nickname)
    await interaction.response.send_message(embed=embed, ephemeral=True)

  @app_commands.command(name = 'moveto', description='Memindahkan user ke channel lain')
  @app_commands.checks.has_permissions(ban_members=True)
  @app_commands.describe(user='User yang ingin dipindahkan', voice_channel='Nama user yang ingin dipindahkan')
  async def moveto(self, interaction: discord.Interaction, user: discord.Member, voice_channel: discord.VoiceChannel):
    embed = discord.Embed(description=f'Memindahkan user dari {user.voice.channel.mention} -> {voice_channel.mention}')
    if not user.voice:
      embed.description = f'❌ User tidak dalam voice channel'
      return await interaction.response.send_message(embed=embed)
    await user.move_to(channel=voice_channel)
    await interaction.response.send_message(embed=embed)
    
  @app_commands.command(name = 'warn', description='Warn user')
  @app_commands.checks.has_permissions(ban_members=True)
  @app_commands.describe(user = 'User yang in di warn')
  async def warn(self, interaction: discord.Interaction, user: discord.Member):
    await check_warn_collection(self.bot, user.id)
    if user.guild_permissions.administrator:
      return await interaction.response.send_message(f'{user.mention} adalah seorang administrator')
    warn_data = await self.bot.warns.find_one({'_id': user.id})
    embed = discord.Embed(color = discord.Color.random())
    embed.description = f'{user.mention} telah di warn!'
    warn_data['total_warn'] += 1
    if warn_data['total_warn'] == 3:
      warn_data['total_warn'] = 0
      warn_data['total_kicked'] += 1
      if warn_data['total_kicked'] == 3:
        embed.description = f'Total di kick yang di miliki {user} udah 3, auto ban'
        await user.ban(reason='Total di kick udah 3, auto ban')
        return await interaction.response.send_message(embed=embed)
      await self.bot.warns.replace_one({'_id': user.id}, warn_data)
      embed.description = f'{user} telah di kick secara otomatis karena mempunya 3 warn.'
      await user.kick(reason='Warn udah 3, auto kick')
      return await interaction.response.send_message(embed=embed)
    embed.set_footer(text=f'{3-warn_data["total_warn"]} warn lagi sebelum auto kick. ')
    await self.bot.warns.replace_one({'_id': user.id}, warn_data)
    await interaction.response.send_message(embed=embed)
    
  @app_commands.command(name = 'clearwarn', description='Clear semua warning')
  @app_commands.describe(user = 'clear warn dari spesifik user')
  @app_commands.checks.has_permissions(ban_members=True)
  async def clearwarn(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
    await check_warn_collection(self.bot, user.id)
    await interaction.response.defer()
    embed = discord.Embed(color = discord.Color.random())
    if user.guild_permissions.administrator:
      return await interaction.response.send_message(f'{user.mention} adalah seorang administrator')
    if user is None:
      total_warn = 0
      all_user_warn = await self.bot.warns.find()
      async for user_warn in all_user_warn.to_list():
        if user_warn['total_warn'] > 0:
          user_warn['total_warn'] = 0
          await self.bot.warns.replace_one({'_id': user_warn['_id']}, user_warn)
          total_warn += 1
      embed.description = f'{total_warn} user telah di clear semua warn nya.'
      return await interaction.followup.send(embed=embed)
    warn_data = self.bot.warns.find_one({'_id': user.id})
    old_total_warn = warn_data['total_warn']
    warn_data['total_warn'] = 0
    embed.description = f'{old_total_warn} warn telah di clear dari {user.mention}.'
    await self.bot.warns.replace_one({'_id': user.id}, warn_data)
    await interaction.followup.send(embed=embed)


  @kick.error 
  @ban.error
  @clearbans.error
  @moveto.error
  @setnickname.error
  @clear.error
  @warn.error
  @clearwarn.error
  async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
      return await interaction.response.send_message('Tidak ada akses.', ephemeral=True)
    elif isinstance(error, app_commands.TransformerError):
       return await interaction.response.send_message('User tidak ditemukan', ephemeral=True)


      
    
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Admin(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])