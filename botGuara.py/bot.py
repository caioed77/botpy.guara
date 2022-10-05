
import asyncio
from fileinput import filename
from http import client
from sys import prefix
from tkinter.messagebox import NO
from urllib import response
import discord
from discord.ext import commands, tasks
import youtube_dl
from random import choice


youtube_dl.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(tittle)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
}

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        
        self.data = data
        self.tittle = data.get("tittle")
        self.url = data.get("url")
    
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )
        
        if "entries" in data:
            data = data["entries"][0]
        
        filename = data["url"] if stream else ytdl.prepare_filename(data)
        
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)            

client = commands.Bot(command_prefix= "?" )

status = ["XVideos", "com JandersIGL", "Programando"]

@client.event
async def on_ready():
    change_status.start()
    print("Bot is Online")
 
@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guil.channels, name="general")
    await channel.send(f"Welcome {member.mention}! Ready to jam out? see`?help` command for details "
    ) 
    
@client.event
async def functions():
    print('Entramos com {0.user}'.format(client))    
    
@client.command(name='ping', help="This is a ping command")
async def ping(ctx):
    await ctx.send(f"**Ping!** Latency :{ round(client.latency * 1000)}ms")

@client.command(name='hello', help="This is a hello command")
async def hello(ctx):
    responses = ["**Resmungar** Por que você me chamou corno?",
                 "Bom dia amigo você e um amigo!",
                 "Oiiii gatinho",
                 "Você e fan do IGL?",
                 "Olá Mestre",
                 ]
    await ctx.send(choice(responses))

@client.command(name="die", help="This command returns a random last word")
async def credits(ctx):
    responses = [
        "why have you brought my short life to an end",
        "I could have done so much more",
        "I have a family, kill them",
    ]
    await ctx.send(choice(responses))
    
@client.command(name='credits', help='This command return the credits')
async def credits(ctx):
    await ctx.send("Feito por `@h1xz#8661` / `Caio Eduardo`")
    
@client.command(name="admin", help="This command return admin")
async def verificaadm(ctx):
    if ctx.author.guild_permissions.administrator:
        await ctx.send('Você é um dos administradores!')
    else:
        await ctx.send('Você não é administrador')

@client.command(nome="dev", help="This command return develop")
async def dev(ctx):
    if ctx.author.id == id:
        await ctx.send(f'Você é o desenvolvedor do Toca Guará!, {ctx.author}')
    else:
        await ctx.send('Você não')

@client.command(name="chines", help="This command chines")
async def chines(ctx):
    verif = 1  
    for verif in range(4):
        if verif == 1 and verif != 2 and verif != 4:
            await ctx.send('Vai toma sua cú')
        else:
            await ctx.send('Porque não Trabalha')
    
        
@client.command(name="play", help="This command plays music")
async def play(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send(" You aren't connect to a voice channel")
        return
    else:
        channel = ctx.message.author.voice.channel
        
    await channel.connect()
    
    server = ctx.message.guild
    voice_channel = server.voice_client
    
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=client.loop)
        voice_channel.play(
            player, after=lambda e: print("Player Erro: %s" % e) if e else None
        )
        
    await ctx.send("**Now Playing:** {}".format(player.tittle))
    
@client.command(name='stop', help='This command stops the music')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()    
    
@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))


client.run("ODgxMzg4NDA4OTg2MDMwMDgx.GUvx3b.xOsVBoVWPgMGSB6_YKxsRctvHNjfXgYly6nOAk")