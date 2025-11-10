# main.py
import os
import asyncio
import functools
import typing
import logging
import discord
from discord import app_commands
from dotenv import load_dotenv
from util import get_response, initialize_conversation_for, reset_conversation

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", "0"))

if not BOT_TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN missing in .env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot")

MY_GUILD = discord.Object(id=GUILD_ID) if GUILD_ID != 0 else None


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        if MY_GUILD:
            self.tree.copy_global_to(guild=MY_GUILD)
            await self.tree.sync(guild=MY_GUILD)
        else:
            await self.tree.sync()


intents = discord.Intents.default()
client = MyClient(intents=intents)


def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper


@client.event
async def on_ready():
    logger.info(f"Logged in as {client.user} (id: {client.user.id})")
    print(f"✅ Logged in as {client.user} (id: {client.user.id})")


@client.tree.command(name="ask", description="Ask the GPT bot a question", guild=MY_GUILD)
@app_commands.describe(prompt="Your question for the AI")
async def ask(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(thinking=True)
    user_id = interaction.user.id
    initialize_conversation_for(user_id)
    result = await asyncio.to_thread(get_response, prompt, user_id)
    await interaction.followup.send(result)


@client.tree.command(name="reset", description="Reset your conversation memory", guild=MY_GUILD)
async def reset(interaction: discord.Interaction):
    user_id = interaction.user.id
    reset_conversation(user_id)
    await interaction.response.send_message("Your conversation memory has been reset.", ephemeral=True)


if __name__ == "__main__":
    client.run(BOT_TOKEN)
