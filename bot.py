import os
import random
import discord
from discord.ext import commands
from discord import app_commands
from quiz_data import QUIZ_QUESTIONS
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Register tree for slash commands
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

@bot.tree.command(name="quiz", description="Start a quiz game")
async def quiz(interaction: discord.Interaction):
    question = random.choice(QUIZ_QUESTIONS)
    options = question["options"]

    view = discord.ui.View()

    # Create buttons for options
    for option in options:
        async def callback(interact, option=option):
            if option == question["answer"]:
                await interact.response.send_message(f"✅ Correct! The answer is **{option}**", ephemeral=False)
            else:
                await interact.response.send_message(f"❌ Wrong! You chose **{option}**", ephemeral=False)

        button = discord.ui.Button(label=option, style=discord.ButtonStyle.primary)
        button.callback = callback
        view.add_item(button)

    embed = discord.Embed(
        title="🎯 Quiz Time!",
        description=question["question"],
        color=discord.Color.blue()
    )

    await interaction.response.send_message(embed=embed, view=view)

bot.run(TOKEN)
