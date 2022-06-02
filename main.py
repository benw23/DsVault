import discord
import requests
import urllib.request
import shutil
import os

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        for g in self.guilds:
            folderName = os.path.join(os.getcwd(), g.name)
            if not os.path.exists(folderName):
                os.makedirs(folderName)
            for c in g.channels:
                if (c.type == discord.ChannelType.text):
                    print("----- "+c.name+" -----")
                    f = open(folderName+"/"+c.name+".htm", 'w')
                    f.write("<h1>"+c.name+"</h1>\n")
                    messages = await c.history(limit=None).flatten()
                    messages = messages[::-1]
                    for m in messages:
                        f.write('<p>{0.author}: {0.content}</p>\n'.format(m))
                        for a in m.attachments:
                            r = requests.get(a.url, stream = True)
                            file_name = a.url.split('/')[-1]
                            with open(folderName+"/"+file_name,'wb') as out_file:
                                shutil.copyfileobj(r.raw, out_file)
                            print(a.url)
                            ext = file_name.split('.')[-1]
                            print(ext)
                            if (ext == 'png' or ext == 'jpg'):
                                print("made it!")
                                f.write('<img src="'+file_name+'"></img>\n')
                            else:
                                f.write(a.url+"\n")
        await self.close()

client = MyClient()
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
