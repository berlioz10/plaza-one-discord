import configparser
import time
from request_status import get_song_details

config = configparser.RawConfigParser()
config.read('discord.properties')

token = config.get('Discord', 'token')

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='po ')

@bot.command(name = 'play')
async def play(message):
    if message.author.voice == None:
        embedVar = discord.Embed(title="Plaza One Radio", description="You need to be in a voice channel to use this command!", color=0xcc0066)
        await message.channel.send(embed=embedVar)
        return

    channel = message.author.voice.channel

    voice = [el for el in message.guild.voice_channels if el.name == channel.name][0]

    voice_client = message.guild.voice_client

    if voice_client == None:
        voice_client = await voice.connect()
    else:
        if voice_client.is_connected() and voice_client.channel == channel:
            embedVar = discord.Embed(title="Plaza One Radio", description="The bot is already on \"" + str(voice_client.channel) + '\" channel', color=0xcc99ff)
            await message.channel.send(embed=embedVar)
            return
            
        await voice_client.move_to(channel)
        
    source = discord.FFmpegPCMAudio("http://radio.plaza.one/mp3", executable="ffmpeg")
    voice_client.play(source, after=None)
    embedVar = discord.Embed(title="Plaza One Radio", description="The bot started playing on \"" + str(message.author.voice.channel) + '\" channel', color=0xcc99ff)
    await message.channel.send(embed=embedVar)

@bot.command(name = 'stop')
async def stop(message):
    voice_client = message.guild.voice_client
    if voice_client != None:
        if voice_client.is_connected():
            voice_client.stop()
            await voice_client.disconnect()
            embedVar = discord.Embed(title="Plaza One Radio", description="The bot left the voice channel \"" + str(voice_client.channel) + '\"', color=0xcc99ff)
            await message.channel.send(embed=embedVar)
    else:
        embedVar = discord.Embed(title="Plaza One Radio", description="The bot is not in a voice channel", color=0xcc0066)
        await message.channel.send(embed=embedVar)

last_status_id = None
last_song_ends_at = None

async def send_status_message(message, replace_last = True):
    global last_status_id, last_song_ends_at
    artist, title, album, seconds, length = get_song_details()
    last_song_ends_at = time.time() + length - seconds - 1

    embedVar = discord.Embed(title="Plaza One Radio", description='Status of the current song:', color=0xcc99ff)
    embedVar.add_field(name="Artist", value=artist, inline=True)
    embedVar.add_field(name="Title", value=title, inline=True)
    embedVar.add_field(name="Album", value=album, inline=False)
    embedVar.add_field(name="Timestamp", value=str(seconds // 60) + ":" + str(seconds % 60) + "/" + str(length // 60) + ":" + str(length % 60), inline=False)

    if replace_last:
        if last_status_id != None:
            message = await message.fetch_message(last_status_id)
            await message.delete()

        message = await message.channel.send(embed=embedVar)

        last_status_id = message.id
    else:
        if last_status_id != None:
            message = await message.fetch_message(last_status_id)
            await message.edit(embed= embedVar)

continue_fetch_status = True

@bot.command(name = 'status')
async def status(message):
    await send_status_message(message=message)

    global continue_fetch_status, last_song_ends_at
    continue_fetch_status = True

    while continue_fetch_status:
        if time.time() > last_song_ends_at:
            await send_status_message(message=message, replace_last= False)
        time.sleep(1)

@bot.command(name = 'status stop')
async def status_stop(_):
    global continue_fetch_status
    continue_fetch_status = False

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

bot.run(token)