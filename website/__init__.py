import os
from flask import Flask, request, render_template
from discord.ext import commands 
import pymongo

async def run(bot: commands.Bot):
  app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'website', 'templates'))
  
  @app.route('/', methods=['GET'])
  async def home():
    return render_template('home.html', bot=bot)
  
  @app.route('/guilds', methods=['GET'])
  async def guilds():
    users_leaderboard = bot.collection.find().sort('money', pymongo.ASCENDING)
    return render_template('guilds.html', bot=bot, users_leaderboard=users_leaderboard)
  
  
  app.run(debug=True)