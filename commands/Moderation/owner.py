import os
import sys
import dotenv
import discord 
from discord.ext import commands 
from discord import app_commands
from handler import reload_all

dotenv.load_dotenv()

class Owner(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    
    
  @app_commands.command(name='echo', description='Ngirim pesan pake bot')
  @app_commands.checks.has_any_role('Owner', 'DEV')
  async def echo(self, interaction: discord.Interaction, message: str):
    await interaction.response.send_message('Mengirim Pesan...', ephemeral=True)
    await interaction.channel.send(message)
    
    
  @app_commands.command(name='reload')
  @app_commands.choices(option = [
    app_commands.Choice(name = 'commands', value=1)
  ])
  @app_commands.checks.has_role('DEV')
  async def reload(self, interaction: discord.Interaction, option: int):
    if option == 1:
      await reload_all(self.bot)
      await interaction.response.send_message(f'Semua command berhasil di reload!', ephemeral=True)
      
  @app_commands.command(name = 'shutdown')
  @app_commands.checks.has_role('DEV')
  async def shutdown(self, interaction: discord.Interaction):
    await interaction.response.send_message('Bot telah di shutdown', ephemeral=True)
    await self.bot.close()
    sys.exit(1)
    
    
  @echo.error 
  async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingAnyRole):
      await interaction.response.send_message('Tidak punya akses.', ephemeral=True)
    
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Owner(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])