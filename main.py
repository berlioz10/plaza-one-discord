import configparser
from threading import Thread
import time
from request_status import get_song_details
from song_model import Song

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
            embedVar = discord.Embed(title="Plaza One Radio", description="The bot is already on **" + str(voice_client.channel) + '** channel', color=0xcc99ff)
            await message.channel.send(embed=embedVar)
        else:
            await voice_client.move_to(channel)
            embedVar = discord.Embed(title="Plaza One Radio", description="The bot moved to **" + str(message.author.voice.channel) + '** channel', color=0xcc99ff)
            await message.channel.send(embed=embedVar)
        return
        
    source = discord.FFmpegPCMAudio("http://radio.plaza.one/mp3", executable="ffmpeg")
    voice_client.play(source, after=None)
    embedVar = discord.Embed(title="Plaza One Radio", description="The bot started playing on **" + str(message.author.voice.channel) + '** channel', color=0xcc99ff)
    await message.channel.send(embed=embedVar)

@bot.command(name = 'stop')
async def stop(message):
    voice_client = message.guild.voice_client
    if voice_client != None:
        if voice_client.is_connected():
            voice_client.stop()
            await voice_client.disconnect()
            embedVar = discord.Embed(title="Plaza One Radio", description="The bot left the voice channel **" + str(voice_client.channel) + '**', color=0xcc99ff)
            await message.channel.send(embed=embedVar)
    else:
        embedVar = discord.Embed(title="Plaza One Radio", description="The bot is not in a voice channel", color=0xcc0066)
        await message.channel.send(embed=embedVar)

last_status_id = None
last_song_ends_at = None
last_song_played:Song = None
status_guilds_connected = []

def create_embed():
    global last_song_played
    embedVar = discord.Embed(title="Plaza One Radio", description='', color=0xcc99ff)
    embedVar.add_field(name="Album", value=last_song_played.album, inline=False)
    embedVar.set_thumbnail(url=last_song_played.img_url)
    embedVar.add_field(name="Artist", value=last_song_played.artist, inline=True)
    embedVar.add_field(name="Title", value=last_song_played.title, inline=True)
    embedVar.add_field(name="Timestamp", value=str(last_song_played.seconds // 60).zfill(2) + ":" + str(last_song_played.seconds % 60).zfill(2)
    + "/" + str(last_song_played.length // 60).zfill(2) + ":" + str(last_song_played.length % 60).zfill(2), inline=False)
    return embedVar

async def send_status_message_without_request(message):
    global last_song_played, last_status_id, last_song_ends_at
    seconds = last_song_played.length - (last_song_ends_at - time.time())
    last_song_played.seconds = int(seconds)
    embedVar = create_embed()

    if last_status_id != None:
        message = await message.fetch_message(last_status_id)
        await message.edit(embed= embedVar)

async def send_status_message(message, replace_last = True):
    global last_status_id, last_song_ends_at, last_song_played
    artist, title, album, seconds, length, img_url = get_song_details()
    last_song_played = Song(artist, title, album, seconds, length, img_url)
    last_song_ends_at = time.time() + length - seconds - 1

    embedVar = create_embed()

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

    global continue_fetch_status, last_song_ends_at

    continue_fetch_status = False
    
    await send_status_message(message=message)

    continue_fetch_status = True

    while continue_fetch_status:
        time.sleep(3)
        if time.time() > last_song_ends_at:
            await send_status_message(message=message, replace_last= False)
        else:
            await send_status_message_without_request(message)

@bot.command(name = 'status_stop')
async def status_stop(_):
    global continue_fetch_status
    continue_fetch_status = False

@bot.command(name = 'test')
async def test(message):
    try:
        time.sleep(10)
        await message.send("Test finished")
    except Exception as ex:
        await message.send(ex)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

bot.run(token)