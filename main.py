import discord
import os
import asyncio
import yt_dlp
import datetime
from discord.ext import commands
from discord import Member
from discord import utils
from discord.ext.commands import has_permissions, MissingPermissions
from apykeys import *

intents = discord.Intents().default()
intents.message_content = True 
intents.members = True
client = commands.Bot(command_prefix = '!', intents=intents)






# letting know when bot is ready to go
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Watching your Mom'))
    print("Bot is now ready for use")
    print("-------------------------")

# welcome users
@client.event
async def on_member_join(member):
       embed_welcome_channel = discord.Embed(
            title="Welcome",
            description=f'To my server. Please follow the rules and have fun. Dont forget to use !hlp and !welcome commands in the chat also go to #rules section'
       )
       embed_welcome_message = discord.Embed(
            title="Hello, I am NewYBot. Happy to see you in our server community!",
       )
       embed_welcome_channel.set_footer(text=f'{member}')
       embed_welcome_channel.set_author(name="NewYBot", icon_url="https://th.bing.com/th/id/OIP.C5v0eJ_tW4UiG9zYK6OWcAHaHa?pid=ImgDet&rs=1")
       await member.send(embed=embed_welcome_message)
       channel = client.get_channel(1159524167788527770)
       await channel.send(embed=embed_welcome_channel)



# basic commands
@client.command()
async def welcome(ctx):
     embed = discord.Embed(
          title="Welcome to our server",
          description="Please use the command !hlp to get help with a commands. Also follow the server rules, do not swear other wise u will get warn and automatically mute for 1 minute"
     )
     embed.set_author(name=f'NewYegor', icon_url="https://image-cdn.hypb.st/https://hypebeast.com/image/2022/11/asap-rocky-real-life-need-for-speed-mercedes-benz-190e-evo-first-look-info-001.jpg?q=75&w=800&cbr=1&fit=max")
    #   client.get_channel('1159524167788527770')
     await ctx.channel.send(embed=embed)     

@client.command()
async def hlp(ctx):
      await ctx.send('!ban_words - showing what you should not use \n !welcome - bot will give you a welcome message \n !play [url] - bot will play music \n !stop - bot will stop music and leave channel \n !pause - bot will pause muisc \n !resume - bot will resume your music')

@client.command()
async def ban_words(ctx):
      await ctx.send('Do not use any swear words or advertisment words, otherwise you will get a warn')

@client.command()
@commands.has_any_role("CREATOR", "ADMIN")
async def kick(ctx, member: discord.Member, reason = None):
    if reason == None:
        await member.kick()
        await ctx.send(f'User {member} has been kicked with no reason')
    else:
        await member.kick(reason=reason)
        await ctx.send(f'User {member} has been kicked for {reason}')
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("You don't have right to kick")

@client.command()
@commands.has_any_role("CREATOR", "ADMIN")
async def ban(ctx, member: discord.Member, reason = None):
    if reason == None:
        await member.ban()
        await ctx.send(f'User {member} has been banned with no reason')
    else:
        await member.ban(reason=reason)
        await ctx.send(f'User {member} has been banned for {reason}')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("You don't have right to ban")

@client.command()
@commands.has_any_role("CREATOR", "ADMIN")
async def mute(ctx, member: discord.Member, timelimit):
     if "s" in timelimit:
          gettime = timelimit.strip("s")
          newtime = datetime.timedelta(seconds=int(gettime))
          await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
          await ctx.send(f'User {member} has been muuted for {timelimit}')
     if "m" in timelimit:
          gettime = timelimit.strip("m")
          newtime = datetime.timedelta(minutes=int(gettime))
          await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
          await ctx.send(f'User {member} has been muuted for {timelimit}')
     if "h" in timelimit:
          gettime = timelimit.strip("h")
          newtime = datetime.timedelta(hours=int(gettime))
          await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
          await ctx.send(f'User {member} has been muuted for {timelimit}')

@mute.error
async def mute_error(ctx, error):
     if isinstance(error, commands.MissingAnyRole):
            await ctx.send("You have no rights to mute people")



# filtering words + panichment
# @client.command()


@client.command()
@commands.has_any_role("CREATOR", "ADMIN")
async def chat_moderation(ctx, mode="on"):
     if mode == "on":
        await ctx.send("Chat moderation is on")
        client.add_listener(on_message, "on_message")
     elif  mode == "off":
         await ctx.send("Chat moderation is off")
         client.remove_listener(on_message, "on_message")

async def auto_mute(member, timelimit):
          newtime = datetime.timedelta(seconds=int(timelimit))
          await member.edit(timed_out_until=discord.utils.utcnow() + newtime)

async def on_message(message):
    ban_words = ["fuck", "FUCK","bitch", "сука", "россия", "член", "хуй", "пидор"]
    content = message.content.lower()
    for word in ban_words:
        if word in message.content:
                await message.delete()
                await message.channel.send('warn')
                await auto_mute(message.author, 60)
                break
             
    await client.process_commands(message)
          
@chat_moderation.error
async def chat_moderation_error(ctx, error):
     if isinstance(error, commands.MissingAnyRole):
          await ctx.send("You have no rights to use this command")



#runnin the bot
client.run(BOT_TOKEN)



    





