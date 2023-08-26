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

        embed = discord.Embed(
            color=0x10e3e3
        )

        embed.add_field(name="Name", value=name, inline=False)
        embed.add_field(name="Currency", value=currency, inline=False)
        embed.add_field(name="Achievement Points", value=achievement_points, inline=False)
        embed.add_field(name="Equations Solved", value=equations_solved, inline=False)
        embed.add_field(name="Highest Stage Solved", value=highest_stage, inline=False)
        embed.add_field(name="Fastest Stage Time", value=fastest_stage, inline=False)
        embed.add_field(name="Highest Solved Answer", value=highest_abs_answer, inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send("Profile data not found.")

bot.run(TOKEN)
