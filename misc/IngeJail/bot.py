import discord
from discord.ext import commands,tasks
import os
import platform
import random
import asyncio
import re 
from discord.ext import commands
from discord.utils import escape_markdown


bot = commands.Bot(command_prefix="_")

async def send_embed(context,title, description, color =  0x00FF00):
    embed = discord.Embed(
                title=title,
                description=description,
                color=color
            )
    await context.send(embed=embed)

@bot.event
async def on_ready():
    bot.loop.create_task(status_task())
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")

async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game("IngeHack !!"))
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Game(f"_help"))
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Game("Team7evn"))
        await asyncio.sleep(60)

@bot.event
async def on_command_completion(ctx):
    fullCommandName = ctx.command.qualified_name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    guild_name = "Private DM "
    if ctx.guild:
        guild_name =ctx.guild.name
    print(
        f"Executed {executedCommand} command in {guild_name} by {ctx.message.author} (ID: {ctx.message.author.id})")

@bot.command(name="ping")
async def ping(context):
    """
    Check if the bot is alive.
    """
    embed = discord.Embed(
        color=0x00FF00
    )
    embed.add_field(
        name="Pong!",
        value=":ping_pong:",
        inline=True
    )
    embed.set_footer(
        text=f"🏓 Pong Don't Catch it if you can!{context.message.author}"
    )
    await context.send(embed=embed)


blacklist=['eval', 'exec','execfile', 'import', 'open', 'os', 'read', 'system', 'write','print']

@commands.dm_only()
@bot.command(name="eval")
async def eval(context, *,arg:commands.clean_content):
    """
    Evaluate a plan to escape from IngeJail
    """
    plan = arg.strip()
    if plan in blacklist:
        image = random.randint(1,3)
        with open(f'wasted_photos/{image}.gif', 'rb') as f:
            picture = discord.File(f)
            await context.send(file=picture)
        await context.send("WASTED !!!")
    else:
        await context.send(str(exec(plan)))

@commands.dm_only()
@bot.command(name="check")
async def check(context):
    """
    Check Position of the Guards 
    """
    await send_embed(context,"The Guards of Today", str(blacklist))


def verify_plan(plan):
    for blacklisted in blacklist:
        if keyword in text:
            return False
    return True
    

TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN == None:
    raise "Server token not found"

bot.run(TOKEN)