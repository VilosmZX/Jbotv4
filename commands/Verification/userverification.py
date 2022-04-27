import asyncio
import os 
import dotenv
import discord 
from discord.ext import commands 
from discord import app_commands

dotenv.load_dotenv()

class Verification(commands.Cog, app_commands.Group, name = 'verification'):
  def __init__(self, bot: commands.Bot):
    self.bot = bot 
    super().__init__()
    
  
  @app_commands.command(name = 'new', description='Create new Verification')
  async def new_verification(self, interaction: discord.Interaction):
    if interaction.user.get_role(968855301359018065) is not None:
      return await interaction.response.send_message('Kamu sudah terverifikasi!', ephemeral=True)
    
    
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send('Check DM!')
    
  
    embed = discord.Embed(description=f'⏸ Verifikasi Pending!\n\nKamu akan mendapatkan role @Verified dalam 30 detik.')
    embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
    embed.set_footer(text='Status: Pending')
    
    msg = await interaction.user.send(embed=embed)
    
    await asyncio.sleep(30)
    
    await interaction.user.add_roles(interaction.guild.get_role(968855301359018065))
    embed = discord.Embed(description=f'✅ Verifikasi Berhasil!\n\nKamu sudah mendapatkan role @Verified')
    embed.set_footer(text='Status: Verified')
    await msg.edit(embed=embed)

    
    
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Verification(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])