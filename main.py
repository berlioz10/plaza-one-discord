import configparser
config = configparser.RawConfigParser()
config.read('discord.properties')

token = config.get('Discord', 'token')

import discord
from discord.ext import commands
# client = discord.Client()

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


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

bot.run(token)