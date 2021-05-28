import discord
from discord.ext import commands
import logging

from discord.ext.commands.core import command
import pypandoc, pdf2image

# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

bot = commands.Bot(command_prefix = ':',description=description)

@bot.event
async def on_ready():
    print(f"Logged on as {bot.user.name}#{bot.user.discriminator}")

async def get_avatar(user:discord.User):
    str = f"![{user.name}]({user.avatar_url_as(format='png',size=32)})"
    return str

@bot.command()
async def move(ctx,start:discord.Message,end:discord.Message,to:discord.TextChannel):
    if (start.created_at > end.created_at):
        start,end = end,start

    await ctx.send(f"Moving text messages to {to.name}")
    
    
        
    async for message in ctx.channel.history(before=end.created_at.replace(microsecond=end.created_at.microsecond+1000),
                                            after=start.created_at.replace(microsecond=start.created_at.microsecond-1000)):
        embed = await get_embed(message)
        await to.send(embed=embed)
        await message.delete()

    await ctx.send("All messages successfully moved!")

async def get_embed(msg:discord.Message):
    embed = discord.Embed()
    embed.set_author(name=msg.author.name,icon_url=msg.author.avatar_url)
    embed.description = msg.content
    for attachment in msg.attachments:
        embed.set_image(url = attachment.url)
    return embed


@bot.command()
async def md(ctx,*,string:str):
    imgs = await render_md(string)
    for img in imgs:
        img = img.crop(box=(300,300,1500,1900))
        img.save("Trash/out.png")
        await ctx.send(file=discord.File("Trash/out.png"))

async def render_md(string:str):
    pypandoc.convert_text(string,'pdf','md',outputfile="Trash/out.pdf")
    images = pdf2image.convert_from_path("Trash/out.pdf")
    return images

with open("token",'r') as tokenfile:
    token = tokenfile.read()

bot.run(token)