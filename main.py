import discord
import requests
import urllib.request
import shutil

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        for g in self.guilds:
            for c in g.channels:
                if (c.type == discord.ChannelType.text):
                    print("----- "+c.name+" -----")
                    f = open(c.name+".htm", 'w')
                    f.write("<h1>"+c.name+"</h1>")
                    messages = await c.history(limit=200).flatten()
                    messages = messages[::-1]
                    for m in messages:
                        f.write('<p>{0.author}: {0.content}</p>'.format(m))
                        for a in m.attachments:
                            r = requests.get(a.url, stream = True)
                            file_name = a.url.split('/')[-1]
                            with open(file_name,'wb') as out_file:
                                shutil.copyfileobj(r.raw, out_file)
                            print(a.url)
                            ext = file_name.split('.')[-1]
                            print(ext)
                            if (ext == 'png' or ext == 'jpg'):
                                print("made it!")
                                f.write('<img src="'+file_name+'"></img>')
                            else:
                                f.write(a.url)
        await self.close()

client = MyClient()
f = open("key.txt")
client.run(f.readline())
