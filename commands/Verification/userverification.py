import asyncio
import os
import random
import string 
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
    verified_roles = interaction.guild.get_role(968855301359018065)
    code = ''.join(random.choice(string.ascii_uppercase) for i in range(6))
    if interaction.user.get_role(968855301359018065) is not None:
      return await interaction.response.send_message('Kamu sudah terverifikasi!', ephemeral=True)
    
    
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send('Check DM!')
    
  
    embed = discord.Embed(description=f'Masukan Code: *{code}*\n\n⏸ Verifikasi Pending!\n\nKamu akan mendapatkan role @Verified')
    embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
    embed.set_footer(text='Status: Pending ( menunggu selama 1 menit )')
    
    msg = await interaction.user.send(embed=embed)
    
    try:
      msg2 = await interaction.client.wait_for('message', timeout=60, check=lambda m: m.author == interaction.user and m.content == code)
      embed.set_footer(text='Status: Verified✅')
      embed.description = f'Code: *{code}*\n\n😁 Verifikasi Berhasil!\n\nKamu telah mendapatkan role @Verified\n'
      await interaction.user.add_roles(verified_roles)
      await msg.edit(embed=embed) 
    except asyncio.TimeoutError:
      embed.set_footer(text='Status: Failed ( kelamaan )')
      await msg.edit(embed=embed)
      
    
    
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Verification(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])