import os
import sys
import asyncio
import random
import logging
from datetime import datetime, timezone

import aiohttp
import discord

BOT_TOKEN = os.getenv("TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
DELAY = os.getenv("DELAY")
VANITY_FILE = os.getenv("VANITY_FILE")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not BOT_TOKEN or not GUILD_ID or not DELAY or not VANITY_FILE:
    print("Missing required environment variables: BOT_TOKEN, GUILD_ID, DELAY, VANITY_FILE")
    sys.exit(1)

try:
    GUILD_ID = int(GUILD_ID)
    DELAY = float(DELAY)
except Exception:
    print("GUILD_ID must be an integer and DELAY must be a number.")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("vanity-rotator")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def post_webhook(session: aiohttp.ClientSession, url: str, message: str):
    payload = {
        "content": message
    }
    try:
        async with session.post(url, json=payload) as resp:
            if resp.status >= 400:
                text = await resp.text()
                logger.warning("Webhook POST failed: %s %s", resp.status, text)
    except Exception as e:
        logger.exception("Webhook POST exception: %s", e)

def load_vanities(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            items = [line.strip() for line in f if line.strip()]
        return items
    except Exception as e:
        logger.exception("Failed to read vanity file: %s", e)
        return []

@client.event
async def on_ready():
    logger.info("Logged in as %s (%s)", client.user, client.user.id)
    client.loop.create_task(_rotate_task())

async def _rotate_task():
    await client.wait_until_ready()
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        logger.error("Guild not found. Ensure the bot is a member of the guild with ID %s", GUILD_ID)
        await client.close()
        return

    if not guild.me:
        logger.error("Could not determine bot member in guild.")
        await client.close()
        return

    if not guild.me.guild_permissions.manage_guild:
        logger.error("Bot lacks Manage Guild permission in target guild. Grant permission and restart.")
        await client.close()
        return

    last = None
    session = aiohttp.ClientSession() if WEBHOOK_URL else None

    try:
        while True:
            vanities = load_vanities(VANITY_FILE)
            if not vanities:
                logger.error("No vanities found in %s. Retrying after delay.", VANITY_FILE)
                await asyncio.sleep(DELAY)
                continue

            choice = random.choice(vanities)
            if len(vanities) > 1:
                attempts = 0
                while choice == last and attempts < 10:
                    choice = random.choice(vanities)
                    attempts += 1

            ts = datetime.now(timezone.utc).astimezone().isoformat()
            try:
                await guild.edit(vanity_code=choice)
                msg = f"[{ts}] Vanity changed to: `{choice}`"
                logger.info(msg)
                if session and WEBHOOK_URL:
                    await post_webhook(session, WEBHOOK_URL, msg)
                last = choice
            except discord.Forbidden:
                logger.error("[%s] Forbidden: missing permissions to change vanity.", ts)
            except discord.HTTPException as e:
                logger.warning("[%s] HTTP error while changing vanity: %s", ts, e)
            except Exception as e:
                logger.exception("[%s] Unexpected error: %s", ts, e)

            await asyncio.sleep(DELAY)
    finally:
        if session:
            await session.close()

if __name__ == "__main__":
    client.run(BOT_TOKEN)
