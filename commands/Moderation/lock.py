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
    self.exception_channel = [969590898260312064, 969786263957807104]
    
    
 
  @app_commands.command(name='textchannel', description='Lock Text Channel')
  @app_commands.checks.has_permissions(manage_channels=True)
  async def textchannel(self, interaction: discord.Interaction, channel: Optional[discord.TextChannel] = None):
    everyone_role = interaction.guild.get_role(756105841429708830)
    if channel is None:
      channel = interaction.channel
    if not channel.permissions_for(everyone_role).send_messages:
      if channel.id in self.exception_channel:
        return await interaction.response.send_message(f'Channel tidak bisa di buka')
      await channel.set_permissions(everyone_role, send_messages=True)
      return await interaction.response.send_message(f'🔓 Channel {channel.mention} berhasil di buka.')
    await channel.set_permissions(everyone_role, send_messages=False)
    return await interaction.response.send_message(f'🔒 Channel {channel.mention} berhasil di lock.')
  

  @textchannel.error 
  async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
      return await interaction.response.send_message(f'Tidak punya akses!', ephemeral=True)

    
async def setup(bot: commands.Bot):
  await bot.add_cog(Lock(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])