# DsVault

Python "bot" with discordpy (https://github.com/Rapptz/discord.py) to generate a local backup of messages and files. This is not meant to be online and respond to commands like a bot, but rather be used as a CLI one-liner that can be scheduled out via `cron` or `at`, etc.

Channels are represented as HTML files, with image attachments embedded with `<img>` tags and other file types linked to with `<a>`.
All file attachments are downloaded and stored in a `/src` directory under each channel's folder.

Backups are stored in a hierarchical structure, `guild-id` -> `category-id` -> `channel-id`.
Under `channel-id` and `category-id` folders, an `index.html` file is generated with anchor links to the categories and channels, respectively, below.

## Usage
```
usage: main.py [-h] [--show] [guild] [category] [channel]

positional arguments:
  guild
  category
  channel

options:
  -h, --help  show this help message and exit
  --show      output what would be backed up
```

## Setup
Go to the <a href="https://discord.com/developers/applications/">Discord Developers Portal</a>.
Create a new application. Under `Bot`, click `Add Bot`. 
Click `Reset Token` and save the new token. You will need to put this in a `key.txt` file in the same directory as the script.
Scroll down to `Message Content Intent` and enable it.

Under `OAuth2` -> `URL Generator`, select the `bot` scope and `Read Messages/View Channels` bot permission.
You can now click on the URL to invite the bot to a server you manage.

## Examples
Using `--show` to view guilds, categories, and channels:
![image](https://user-images.githubusercontent.com/37031448/200694714-8d2f1f2c-79b8-4086-b7dc-094c3e35d533.png)

Backing up an entire guild:
![image](https://user-images.githubusercontent.com/37031448/200694839-98ed21a7-bf96-4695-a44b-7661af0ea179.png)

Backing up a single channel:
![image](https://user-images.githubusercontent.com/37031448/200694910-6b2daed8-398b-49a2-92a8-a50e5636b2c9.png)

Example `index.html` for guild:

![image](https://user-images.githubusercontent.com/37031448/200695018-0d861e69-c9e5-415c-b1ea-413ed022c2c7.png)

Example `index.html` for channel:

![image](https://user-images.githubusercontent.com/37031448/200907252-7e89f9f5-7fe7-4453-896d-53bbd23e0908.png)


