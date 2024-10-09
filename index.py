import os
import discord # type: ignore
from dotenv import load_dotenv # type: ignore
from commands.DatabaseCommand import DatabaseCommand
from commands.PingCommand import PingCommand
from events.MessageEvent import MessageEvent
from events.onReady import onReady
from helpers.ColorHelper import ColorHelper
from helpers.DatabaseChecker import DatabaseChecker

ColorHelper.print_colored_message("Starting the bot...", "gray")
ColorHelper.print_colored_message("Loading env...", "gray")
load_dotenv()
ColorHelper.print_colored_message("Env loaded", "green")


discord_token = os.getenv("TOKEN")
activity_message = os.getenv("ACTIVITY")
register_commands = os.getenv("REGISTER_COMMANDS_ONLY_GUILD")

# Intents
ColorHelper.print_colored_message("Setting up intents...", "gray")
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
ColorHelper.print_colored_message("Intents set up", "green")

ColorHelper.print_colored_message("Initializing the bot...", "gray")
# Initialize the bot
client = discord.Bot(
    command_prefix=">", 
    activity=discord.Game(name=activity_message), 
    intents=intents
)

ColorHelper.print_colored_message("Bot initialized", "green")

# Check databases
ColorHelper.print_colored_message("Checking databases...", "gray")
try:
    DatabaseChecker.checkAll()
    ColorHelper.print_colored_message("Databases checked", "green")
except Exception as e:
    ColorHelper.print_colored_message(f"Error checking dbs: {e}", "red")
    exit()


# Register events
onReady(client)
MessageEvent(client)

# Register commands
DatabaseCommand(client)
PingCommand(client)

client.run(discord_token)