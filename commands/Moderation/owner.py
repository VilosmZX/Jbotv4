import os
import dotenv
import discord 
from discord.ext import commands 
from discord import app_commands

dotenv.load_dotenv()

class Owner(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    
    
  @app_commands.command(name='echo', description='Ngirim pesan pake bot')
  @app_commands.checks.has_any_role('Owner', 'DEV')
  async def echo(self, interaction: discord.Interaction, message: str):
    await interaction.response.send_message('Mengirim Pesan...', ephemeral=True)
    await interaction.channel.send(message)
    
    
  @echo.error 
  async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingAnyRole):
      await interaction.response.send_message('Tidak punya akses.', ephemeral=True)
    
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Owner(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])