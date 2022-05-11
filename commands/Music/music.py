import discord
import wavelink
from discord.ext import commands
from discord import ChannelType
from discord.abc import GuildChannel
from discord import app_commands
import os


class Music(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot


  @app_commands.command(name = 'play', description='Memainkan musik')
  @app_commands.describe(search = 'Cari Video atau Lagu')
  async def play(self, interaction: discord.Interaction, search: str):
    embed = discord.Embed(color=discord.Color.random())
    search = await wavelink.YouTubeTrack.search(query=search, return_first=True)
    if getattr(interaction.user.voice, 'channel', None) is None:
      embed.description = f'Kamu harus masuk ke dalam voice channel!!!'
      return await interaction.response.send_message(embed=embed)
    if not interaction.guild.voice_client:
      vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
    else:
      vc: wavelink.Player = interaction.guild.voice_client

    if vc.queue.is_empty and not vc.is_playing():
      await vc.play(search)
      embed.description = f'Memainkan {search.title}'
      await interaction.response.send_message(embed=embed)
    else:
      await vc.queue.put_wait(search)
      embed.description = f'Menambahkan {search.title} ke dalam antrian'
      await interaction.response.send_message(embed=embed)


  @app_commands.command(name = 'pause', description='Stop lagu')
  async def pause(self, interaction: discord.Interaction):
    embed = discord.Embed(color = discord.Color.random())
    if getattr(interaction.user.voice, 'channel', None) is None:
      embed.description = f'Kamu harus masuk ke dalam voice channel!!!'
      return await interaction.response.send_message(embed=embed)
    if not interaction.guild.voice_client:
      vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
    else:
      vc: wavelink.Player = interaction.guild.voice_client

    if vc.is_paused():
      embed.description = f'Sudah dalam mode pause'
      return await interaction.response.send_message(embed=embed)
    await vc.pause()

  @app_commands.command(name='resume', description='Stop lagu')
  async def resume(self, interaction: discord.Interaction):
    embed = discord.Embed(color=discord.Color.random())
    if getattr(interaction.user.voice, 'channel', None) is None:
      embed.description = f'Kamu harus masuk ke dalam voice channel!!!'
      return await interaction.response.send_message(embed=embed)
    if not interaction.guild.voice_client:
      vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
    else:
      vc: wavelink.Player = interaction.guild.voice_client

    if vc.is_paused():
      await vc.resume()
      embed.description = f'Berhasil di lanjutkan'
      return await interaction.response.send_message(embed=embed)

  @app_commands.command(name='volume', description='Stop lagu')
  async def volume(self, interaction: discord.Interaction, volume: int):
    embed = discord.Embed(color=discord.Color.random())
    if getattr(interaction.user.voice, 'channel', None) is None:
      embed.description = f'Kamu harus masuk ke dalam voice channel!!!'
      return await interaction.response.send_message(embed=embed)
    if not interaction.guild.voice_client:
      vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
    else:
      vc: wavelink.Player = interaction.guild.voice_client

    await vc.set_volume(volume)


async def setup(bot: commands.Bot):
  await bot.add_cog(Music(bot), guilds=[discord.Object(id=os.environ.get('GUID'))])


        