import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from intro import delve_game
from database import get_profile_data

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


@bot.command()
async def profile(ctx):
    user_id = str(ctx.author.id)
    profile_data = get_profile_data(user_id)

    if profile_data:
        name = profile_data['name']
        currency = profile_data['currency']
        achievement_points = profile_data['achievement_points']
        equations_solved = profile_data['equations_solved']
        highest_stage = profile_data['highest_stage']
        fastest_stage = profile_data['rounded_fastest_time']
        highest_abs_answer = profile_data['new_highest_abs_answer']

        profile_message = (
            f"Name: {name}\n"
            f"Currency: {currency}\n"
            f"Achievement Points: {achievement_points}\n"
            f"Equations Solved: {equations_solved}\n"
            f"Highest Stage Solved: {highest_stage}\n"
            f"Fastest Stage Time: {fastest_stage}\n"
            f"Highest Solved Answer: {highest_abs_answer}\n"
        )
    else:
        profile_message = "Profile data not found."

    await ctx.send(profile_message)  # Send a user's profile.

bot.run(TOKEN)
