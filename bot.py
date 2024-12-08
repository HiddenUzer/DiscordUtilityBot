import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

# Load environment variables from the .env file
load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Load bot token securely from .env

# Initialize bot intents and bot instance
intents = discord.Intents.default()
intents.members = True  # Enable member events
bot = commands.Bot(command_prefix="/", intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} ({bot.user.id})")
    await bot.tree.sync()
    print("✅ Slash commands synced.")

# Event: Member joins
@bot.event
async def on_member_join(member):
    try:
        # Create a personalized welcome message
        welcome_message = (
            f"👋 Welcome to **{member.guild.name}**, {member.mention}!\n\n"
            "We're happy to have you here! If you're interested in trying our product, we can offer you a vouch key."
        )
        # Send the DM to the new member
        await member.send(welcome_message)
        print(f"✅ Sent a welcome DM to {member.name}.")
    except discord.Forbidden:
        print(f"⚠️ Could not send a DM to {member.name}. They might have DMs disabled.")
    except Exception as e:
        print(f"❌ Error sending DM to {member.name}: {e}")

# Slash command: Ban a member
@bot.tree.command(name="ban", description="Ban a member from the server.")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"🚨 {member.mention} has been banned for: {reason}")
    except discord.Forbidden:
        await interaction.response.send_message("❌ I do not have permission to ban this user.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"❌ An error occurred while banning the user: {e}", ephemeral=True)

# Entry point: Run the bot
if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌ Bot token not found. Please ensure it is set in the .env file.")
    else:
        try:
            bot.run(BOT_TOKEN)
        except discord.LoginFailure:
            print("❌ Invalid bot token. Please verify the token in the .env file.")
