import os
import discord
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv
from intro import play_game
from database import get_profile_data, leaderboard_data, get_achievements_data, get_achievement_desc, unlock_shop_access, get_energy_info, get_energy_max_info
from shop import veggie_stall_items, shop_access

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.typing = True
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

# Removing the default name commands to avoid conflicts
bot.remove_command('help')


# Setting the bot ready up and down


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="with the abyss"))  # Set bots activity
    channel = bot.get_channel(1181867609285726238)  # Replace with the actual channel ID
    if channel:
        # Check if there are any previous messages by the bot in the channel
        async for message in channel.history(limit=None):
            if message.author == bot.user:
                # If there's a previous message by the bot, edit it
                await message.edit(
                    content=f"```Current bot status: ONLINE\nOnline since: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC```")
                break
        else:
            # If no previous message, send a new one
            await channel.send(
                f"```Current bot status: ONLINE\nOnline since: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC```")


@bot.command()
async def kill(ctx):
    admin_id = int(os.getenv('USER_ID'))
    admin_channel = int(os.getenv('ADMIN'))
    channel = bot.get_channel(1181867609285726238)
    if ctx.author.id == admin_id and ctx.channel.id == admin_channel:
        await ctx.send("Turning off the bot...")
        if channel:
            async for message in channel.history(limit=None):
                if message.author == bot.user:
                    await message.edit(
                        content=f"```Current bot status: OFFLINE\nOffline since: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC```")
        print(f'{bot.user} successfully shut down!')
        await bot.close()
    else:
        await ctx.send("You don't have permissions to use this commend!")


# Various delve modes section


@bot.command()
async def delve(ctx):
    ruleset = "delve"
    game_output = await play_game(ctx, bot, ruleset)  # Classic delve gamemode
    await ctx.send(game_output)


@bot.command()
async def tld(ctx):
    ruleset = "tld"
    game_output = await play_game(ctx, bot, ruleset)  # Time-Limited delve gamemode
    await ctx.send(game_output)


@bot.command()
async def challenge(ctx):
    discord_id = ctx.author.id

    nrg_v_value = get_energy_info(discord_id)

    if nrg_v_value > 0:
        ruleset = "challenge"
        game_output = await play_game(ctx, bot, ruleset)  # Challenge delve gamemode
        await ctx.send(game_output)
    else:
        await ctx.send("You don't have enough {energy resource} to challenge for now.")


@bot.command()
async def check(ctx, arg=None):
    discord_id = ctx.author.id  # Get user's Discord ID
    if arg is None:
        user = ctx.author
    else:
        try:
            user = await commands.MemberConverter().convert(ctx, arg)
        except commands.MemberNotFound:
            await ctx.send("User not found.")
            return

    # Fetch NRG_V, NRG_M from the database using get_energy_info and get_energy_max_info functions
    nrg_v = get_energy_info(discord_id)
    nrg_m = get_energy_max_info(discord_id)

    embed = discord.Embed(
        title="Energy Status",
        color=0x992D22
    )
    embed.set_thumbnail(url=user.avatar.url)  # Set user's avatar as thumbnail
    embed.add_field(name="Energy", value=f"{nrg_v} / {nrg_m}", inline=True)
    await ctx.send(embed=embed)


# Account Commands


@bot.command()
async def profile(ctx, arg=None):
    if arg is None:
        user = ctx.author
    else:
        try:
            user = await commands.MemberConverter().convert(ctx, arg)
        except commands.MemberNotFound:
            await ctx.send("User not found.")
            return

    profile_data = get_profile_data(user.name)

    if profile_data:
        name = profile_data['name']
        currency = profile_data['FreeC']
        chall_currency = profile_data['ChallC']
        achievement_points = profile_data['achievement_points']
        equations_solved = profile_data['equations_solved']
        highest_stage = profile_data['highest_stage']
        fastest_stage = profile_data['rounded_fastest_time']
        highest_abs_answer = profile_data['new_highest_abs_answer']

        embed = discord.Embed(
            title="Profile",
            color=0x10e3e3
        )

        embed.set_thumbnail(url=user.avatar.url)  # Set user's avatar as thumbnail

        embed.add_field(name="Name", value=name, inline=False)
        embed.add_field(name="FC (Free Curr.)", value=currency, inline=False)
        embed.add_field(name="CC (Chall Curr.)", value=chall_currency, inline=False)
        embed.add_field(name="Achievement Points", value=achievement_points, inline=False)
        embed.add_field(name="Equations Solved", value=equations_solved, inline=False)
        embed.add_field(name="Highest Stage Solved", value=highest_stage, inline=False)
        embed.add_field(name="Fastest Stage Time", value=fastest_stage, inline=False)
        embed.add_field(name="Highest Solved Answer", value=highest_abs_answer, inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send("Profile data not found. Create one by delving once.")


@bot.command()
async def leaderboard(ctx):
    leaderboard = leaderboard_data()
    name0 = leaderboard['name0']
    name1 = leaderboard['name1']
    name2 = leaderboard['name2']
    name3 = leaderboard['name3']
    name4 = leaderboard['name4']
    name5 = leaderboard['name5']
    name6 = leaderboard['name6']
    name7 = leaderboard['name7']
    name8 = leaderboard['name8']
    name9 = leaderboard['name9']

    highest0 = leaderboard['highest0']
    highest1 = leaderboard['highest1']
    highest2 = leaderboard['highest2']
    highest3 = leaderboard['highest3']
    highest4 = leaderboard['highest4']
    highest5 = leaderboard['highest5']
    highest6 = leaderboard['highest6']
    highest7 = leaderboard['highest7']
    highest8 = leaderboard['highest8']
    highest9 = leaderboard['highest9']

    record0 = str("#1: **") + name0 + str(" (") + str(highest0) + str(")**\n")
    record1 = str("#2: **") + name1 + str(" (") + str(highest1) + str(")**\n")
    record2 = str("#3: **") + name2 + str(" (") + str(highest2) + str(")**\n")
    record3 = str("#4: **") + name3 + str(" (") + str(highest3) + str(")**\n")
    record4 = str("#5: **") + name4 + str(" (") + str(highest4) + str(")**\n")
    record5 = str("#6: **") + name5 + str(" (") + str(highest5) + str(")**\n")
    record6 = str("#7: **") + name6 + str(" (") + str(highest6) + str(")**\n")
    record7 = str("#8: **") + name7 + str(" (") + str(highest7) + str(")**\n")
    record8 = str("#9: **") + name8 + str(" (") + str(highest8) + str(")**\n")
    record9 = str("#10: **") + name9 + str(" (") + str(highest9) + str(")**")

    leaderboard_text = record0 + record1 + record2 + record3 + record4 + record5 + record6 + record7 + record8 + record9

    embed = discord.Embed(
        title="EquationEvo Leaderboard",
        color=0x32cd32
    )
    embed.add_field(name="", value=leaderboard_text)

    await ctx.send(embed=embed)


@bot.command()
async def achievements(ctx, arg=None):
    if arg is None:
        user_name = str(ctx.author.name)
    else:
        user_name = str(arg)

    achievements_data = get_achievements_data(user_name)

    embed = discord.Embed(
        title="Unlocked Achievements",
        color=0xff7f7f
    )

    embed.add_field(name="", value=achievements_data)

    await ctx.send(embed=embed)


@bot.command()
async def whatis(ctx, arg=None):
    if arg is None:
        await ctx.send("Put a command as an argument (ex. **!whatis \"Initiating the Dive\"**)")
    else:
        achievement_name = str(arg)

        achievement_desc = get_achievement_desc(achievement_name)

        embed = discord.Embed(
            title=arg,
            color=0xb1a29d
        )

        embed.add_field(name="", value=achievement_desc)

        await ctx.send(embed=embed)

# Shop Commands


@bot.command()
async def shop(ctx):
    # Get user's data
    user_name = str(ctx.author.name)
    profile_data = get_profile_data(user_name)

    if not profile_data:
        await ctx.send("Profile data not found. Create one by delving once.")
        return

    # Checking if user can access the shop
    if not shop_access(profile_data):
        if isinstance(ctx.channel, discord.TextChannel):
            await ctx.send("Beyond the veil of ignorance, the Emporium's allure stays hidden, awaiting your descent "
                           "into the abyss of revelation.")
        return

    # Display the shop selection message in a direct message
    user = ctx.author
    selection_embed = discord.Embed(
        title="Select Shop",
        description="Please select type of shop.",
        color=0x9400D3,
    )

    selection_message = await user.send(embed=selection_embed)

    # Add button for Veggie Stall
    selection_view = discord.ui.View()

    async def on_veggie_stall(interaction: discord.Interaction):
        # Display Veggie Stall items in the embed
        veggie_stall_embed = discord.Embed(
            title="Veggie Stall",
            description="Welcome to the Veggie Stall.",
            color=0x008000,  # Green color for veggies
        )
        for item in veggie_stall_items:
            veggie_stall_embed.add_field(
                name=item["name"],
                value=f"{item['description']}\nPrice: {item['price']} currency",
                inline=False,
            )
        await interaction.response.send_message(embed=veggie_stall_embed, ephemeral=True)

    veggie_stall_button = discord.ui.Button(label="Veggie Stall", style=discord.ButtonStyle.grey, emoji="🫑")
    veggie_stall_button.callback = on_veggie_stall
    selection_view.add_item(veggie_stall_button)

    await selection_message.edit(embed=selection_embed, view=selection_view)

    if isinstance(ctx.channel, discord.TextChannel):
        await ctx.send("Only in solitude may the Emporium's mysteries be revealed. The enigmatic proprietor shuns all "
                       "witnesses but the chosen.")


@bot.command()
async def unlock_shop(ctx):
    # Getting user data
    user_id = ctx.author.id
    profile_data = get_profile_data(ctx.author.name)

    if not profile_data:
        await ctx.send("Profile data not found. Create one by delving once.")
        return

    # Checking if user can unlock the shop
    if (profile_data.get("highest_stage", 0) >= 9 and profile_data.get("currency", 0) >= 2000 and profile_data.get
            ("shop_access", 0) == 0):
        await unlock_shop_access(user_id)
        await ctx.send("Congratulations, unlocker of secrets. The Emporium's enigmatic embrace now welcomes your "
                       "presence.")
    else:
        await ctx.send("The Emporium's gatekeeper discerns worthiness in the hearts of seekers. Approach only if your "
                       "purpose resonates with the enigmatic path it guards.")


@bot.command()
async def help(ctx):
    help_embed = discord.Embed(
        title="Bot Commands",
        description="List of commands usable by <@1143308488487993364>",
        color=0x8080
    )

    # Delving Modes Section
    help_embed.add_field(
        name="**Delving Modes:** \n!delve",
        value="Classic delving experience",
        inline=False
    )
    help_embed.add_field(
        name="!tld",
        value="Delving with one non-regenerable timer",
        inline=False
    )

    # Account Commands Section
    help_embed.add_field(
        name="**Account Commands:** \n!profile (username)",
        value="Displays the profile of the user",
        inline=False
    )
    help_embed.add_field(
        name="!leaderboard",
        value="Displays the highest achieved floors with users who achieved that",
        inline=False
    )
    help_embed.add_field(
        name="!achievements",
        value="Displays user's achievements",
        inline=False
    )
    help_embed.add_field(
        name="!whatis \"Name of the achievement\"",
        value="Shows how to get an achievement",
        inline=False
    )

    await ctx.send(embed=help_embed)

bot.run(TOKEN)
