import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from intro import delve_game

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.typing = True
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="with the abyss"))  # Set bots activity
    channel = bot.get_channel(1133542620551987361)  # Replace with the actual channel ID
    if channel:
        await channel.send("<@213540116386414592> It's delving time!")


@bot.command()
async def delve(ctx):
    game_output = await delve_game(ctx, bot)  # Call the delve function without any parameters
    await ctx.send(game_output)   # Send the game output as a message in the channel

bot.run(TOKEN)