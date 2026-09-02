import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from queries import get_latest_snapshot,get_repo_history
from data_vis import generate_star_trend_chart

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


@bot.tree.command(name="stats", description="Get latest stats for a repo")
async def stats(interaction: discord.Interaction, owner: str, name: str):
    df = get_latest_snapshot(owner, name)
    if df.empty:
        await interaction.response.send_message(f"No data found for {owner}/{name}")
        return

    row = df.iloc[0]
    await interaction.response.send_message(
        f"**{owner}/{name}**\n"
        f"⭐ {row['stars']} stars | 🍴 {row['forks']} forks | "
        f"🐛 {row['open_issues']} issues\n"
        f"_as of {row['captured_at']}_"
    )


@bot.tree.command(name="trend", description="Show star growth over time")
async def trend(interaction: discord.Interaction, owner: str, name: str):
    df = get_repo_history(owner, name)
    if df.empty:
        await interaction.response.send_message(f"No data found for {owner}/{name}")
        return
    if len(df) < 2:
        await interaction.response.send_message(
            f"Only one snapshot recorded for {owner}/{name} so far — run the pipeline "
            f"a few more times to build up trend data."
        )
        return

    await interaction.response.defer()  # chart generation may take a moment
    chart_path = generate_star_trend_chart(df, owner, name)
    await interaction.followup.send(file=discord.File(chart_path))


if __name__ == "__main__":
    bot.run(TOKEN)