import discord
import requests
import urllib.request
import shutil
import os
import random
import argparse
import asyncio
import platform

if platform.system() == 'Windows':
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
ROOT_DIR = os.path.realpath(os.path.dirname(__file__))

def printGuilds(guilds):
    print("This bot is a member of the following servers:")
    for g in guilds:
        print("{} : {}".format(g.id, g))

def printCategories(guild):
    print(guild)
    print("------")
    for c in guild.categories:
        print("{} : {}".format(c.id, c))
    print()

def printChannels(category):
    print(category)
    print("------")
    for chan in category.channels:
        if (chan.type == discord.ChannelType.text):
            print("{} : {}".format(chan.id, chan))
    print()

async def backupGuild(guild):
    print("backing up guild {} : {}".format(guild.id, guild))

    folderName = os.path.join(ROOT_DIR, str(guild.id))
    if not os.path.exists(folderName):
        os.makedirs(folderName)

    f = open(folderName+"/index.htm", 'w', encoding="utf-8")
    f.write("<h1>"+guild.name+"</h1>\n<ul>\n")

    for category in guild.categories:
        f.write("<li><a href='{}'>{}</a></li>\n<ul>\n".format(str(category.id)+"/index.htm", category.name))
        for channel in category.channels:
            f.write("<li><a href='{}'>{}</a></li>\n".format(str(category.id)+"/"+str(channel.id)+"/index.htm", channel.name))
        f.write("</ul>\n")
        f.close()
        f = open(folderName+"/index.htm", 'a',  encoding="utf-8")
        await backupCategory(category)

    f.write("</ul>")
    f.close()
    return

async def backupCategory(category):
    print("--- backing up category {} : {}".format(category.id, category))

    rootFolder = os.path.join(ROOT_DIR, str(category.guild.id))
    folderName = rootFolder+"/"+str(category.id)
    if not os.path.exists(folderName):
        os.makedirs(folderName)

    f = open(folderName+"/index.htm", 'w', encoding="utf-8")
    f.write(f"<h1>\n<a href='../index.htm'>{ category.guild.name }</a> / { category.name } \n</h1>\n\n<ul>\n")

    for channel in category.channels:
        if channel.type == discord.ChannelType.text:
            f.write(f"<li><a href='{ channel.id }'>{ channel.name }</a></li>\n")
            await backupChannel(channel)

    f.write("</ul>")
    f.close()
    return

async def backupChannel(channel):
    print("------ backing up channel {} : {}".format(channel.id, channel))

    rootFolder = os.path.join(ROOT_DIR, str(channel.guild.id))
    folderName = rootFolder+"/"+str(channel.category.id)+"/"+str(channel.id)
    if not os.path.exists(folderName):
        os.makedirs(folderName)

    f = open(folderName+"/index.htm", 'w', encoding="utf-8")

    f.write("<h1>\n")
    f.write(f"<a href='../../index.htm'>{ channel.guild.name }</a> / \n")
    f.write(f"<a href='../index.htm'>{ channel.category.name }</a> / { channel.name }\n")
    f.write("</h1>\n\n")


    srcName = os.path.join(folderName, "src")
    if not os.path.exists(srcName):
        os.makedirs(srcName)

    out = []
    async for m in channel.history(limit=None):
        thisLine = ""
        thisLine += f'<p>{ m.author.name }: { m.content }'

        for a in m.attachments:
            r = requests.get(a.url, stream = True)
            file_name = a.url.split('/')[-1]
            ext = file_name.split('.')[-1]

            # if the file name already exists, append a random number
            # from 0-9 until the file does not exist
            fullPath = os.path.join(srcName, file_name)
            while os.path.exists(fullPath):
                i = file_name.rfind('.')
                file_name = file_name[:i] + str(random.randint(0,9)) + file_name[i:]
                fullPath = os.path.join(srcName, file_name)

            with open(folderName+"/src/"+file_name,'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
            print(a.url)
            if (ext == 'png' or ext == 'jpg' or ext == 'jpeg' or ext == 'gif'):
                thisLine += '<img src="src/'+file_name+'"></img>'
            else:
                thisLine += f'<a href="src/{ file_name }">{ file_name }</a>'
        thisLine += '</p>\n'
        out.append(thisLine)
    for o in out[::-1]:
        f.write(o)
    f.close()

    return

class MyClient(discord.Client):
    async def on_ready(self):
        print('Successfully authenticated as {0}'.format(self.user))
        if args.show:
            if not args.guild:
                printGuilds(self.guilds)
            elif not args.category:
                g = self.get_guild(args.guild)
                if g:
                    printCategories(g)
                else:
                    print("Guild does not exist")
            elif not args.channel:
                g = self.get_guild(args.guild)
                if g:
                    c = g.get_channel(args.category)
                    if c:
                        printChannels(c)
                    else:
                        print("Channel does not exist")
                else:
                    print("Guild does not exist")
        else:
            if not args.category:
                g = self.get_guild(args.guild)
                if g:
                    await backupGuild(g)
                else:
                    print("Guild does not exist")
            elif not args.channel:
                g = self.get_guild(args.guild)
                if g:
                    c = g.get_channel(args.category)
                    if c:
                        await backupCategory(c)
                    else:
                        print("Channel does not exist")
                else:
                    print("Guild does not exist")
            else:
                g = self.get_guild(args.guild)
                if g:
                    c = g.get_channel(args.channel)
                    if c:
                        await backupChannel(c)
                    else:
                        print("Channel does not exist")
                else:
                    print("Guild does not exist")
        await self.close()

## PARSE ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument("--show", help="output what would be backed up", action="store_true")
parser.add_argument('guild', nargs='?', type=int)
parser.add_argument('category', nargs='?', type=int)
parser.add_argument('channel', nargs='?', type=int)
args = parser.parse_args()

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

if not args.guild and not args.show:
    print("Please specify a guild. Use -h or --help to see options.")
    quit()

## READ IN API KEY
try:
    with open("key.txt", "r") as f:
        content = f.read()
    if not content:
        print("key.txt is empty")
    else:
        client.run(content)
except IOError as e:
    if e.errno == 2:
        print("key.txt does not exist")
    else:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
except:
   print("Unexpected error:", sys.exc_info()[0])
