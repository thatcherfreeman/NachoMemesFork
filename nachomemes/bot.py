import argparse
import asyncio
import io
import json
import os
import random
import re
import sys
import textwrap
import traceback
import uuid
from datetime import datetime, timedelta
from typing import Iterable
from pathlib import Path

import discord
import psutil
from discord.ext import commands
from discord.ext.commands import Context, has_permissions

from dynamo import DynamoTemplateStore
from localstore import LocalTemplateStore
from render import MemeTemplate, TextBox
from store import Store, TemplateError

description = "A bot to generate custom memes using pre-loaded templates."
bot = commands.Bot(command_prefix="/", description=description)

# Used for calculating memes/minute.
global MEMES
MEMES = 0

# Base directory from which paths should extend.
global BASE_DIR
BASE_DIR = Path(__file__).parent.parent


@bot.event
async def on_ready():
    print("Only memes can melt steel beams.\n\t--Shia LaBeouf")
    bot.loop.create_task(status_task())


with open(os.path.join(BASE_DIR, "config/messages.json"), "rb") as c:
    statuses = json.load(c)["credits"]


@bot.event
async def status_task():
    while True:
        global MEMES
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game(
                name=f"{MEMES} memes/minute! "
                + "Load AVG - CPU: {0:.2f}% ".format(psutil.getloadavg()[0])
                + "RAM: {0:.2f}% ".format(psutil.virtual_memory()._asdict()["percent"])
            ),
        )
        MEMES = 0
        await asyncio.sleep(60)


@bot.command(description="List templates.")
async def templates(ctx, template=None):
    try:
        guild = str(ctx.message.guild.id)
        if template:
            meme = store.read_meme(guild, template)
            await ctx.send(
                textwrap.dedent(
                    f"""\
                Name: {meme.name}
                Description: *{meme.description}*
                Times used: {meme.usage}
                Expects {len(meme.textboxes)} strings
                Read more: {meme.docs}"""
                )
            )
        else:
            await ctx.send(
                "== Templates =="
                + "".join(
                    f"\n{meme['name']}: *{meme['description']}*"
                    for meme in store.list_memes(guild, ("name", "description"))
                )
            )
    except TemplateError:
        await ctx.send(f"```Could not load '{template}'```")
    except:
        err = traceback.format_exc()
        if testing:
            await ctx.send("```" + err[:1990] + "```")
        print(err, file=sys.stderr)


# Only allows an administrator to refresh templates.
@bot.command(description="refresh templates.")
@has_permissions(administrator=True)
async def refresh_templates(ctx: Context, arg: str = None):
    try:
        await ctx.trigger_typing()
        guild = str(ctx.message.guild.id)
        message = store.refresh_memes(guild, arg == "--hard")
        await ctx.send(f"```{message}```")
    except:
        err = traceback.format_exc()
        if testing:
            await ctx.send("```" + err[:1990] + "```")
        print(err, file=sys.stderr)


@bot.command(description="Make a new meme.")
async def meme(ctx: Context, template: str, *text):
    await ctx.trigger_typing()
    try:
        # Log memes/minute.
        global MEMES
        MEMES += 1
        # Case insensitive meme naming
        template = template.lower()
        meme = store.read_meme(
            str(ctx.message.guild.id)
            if ctx.message.guild != None
            else "nachomemes-default",
            template,
            True,
        )
        # Have the meme name be reflective of the contents.
        name = re.sub(r"\W+", "", str(text))
        key = f"{template}-{name}.png"

        with io.BytesIO() as buffer:
            meme.render(text, buffer)
            buffer.flush()
            buffer.seek(0)
            msg = await ctx.send(file=discord.File(buffer, key))
        if random.randrange(8) == 0:
            tmpmsg = msg
            e = discord.Embed().set_image(url=tmpmsg.attachments[0].url)
            e.set_footer(text=random.choice(statuses))
            msg = await ctx.send(embed=e)
            await tmpmsg.delete()
        for r in ("\N{THUMBS UP SIGN}", "\N{THUMBS DOWN SIGN}"):
            await msg.add_reaction(r)
    except TemplateError:
        await ctx.send(f"```Could not load '{template}'```")
    except:
        err = traceback.format_exc()
        if testing:
            await ctx.send("```" + err[:1990] + "```")
        print(err, file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Runs the bot passed on input parameters."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Whether or not to run the bot in debug mode.",
    )
    parser.add_argument(
        "--local", action="store_true", help="Force running without Dynamo."
    )
    args = parser.parse_args()
    global testing
    testing = args.debug

    try:
        creds_file_name = (
            "config/creds.json" if not testing else "config/testing-creds.json"
        )
        with open(os.path.dirname(__file__) + "/../" + creds_file_name, "rb") as f:
            creds = json.load(f)
    except:
        creds = {}
    for k in ("DISCORD_TOKEN", "ACCESS_KEY", "SECRET", "REGION"):
        if k in os.environ:
            creds[k.lower()] = os.environ[k]

    global store
    store = LocalTemplateStore()
    if not args.local and "access_key" in creds:
        store = DynamoTemplateStore(
            creds["access_key"], creds["secret"], creds["region"], store, args.debug
        )

    try:
        token = creds["discord_token"]
    except NameError:
        print(
            "Could not get Discord token from config/creds.json environment variable $DISCORD_TOKEN!"
        )
        sys.exit(1)

    bot.run(token)