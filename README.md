# DsVault

Python "bot" with discordpy (https://github.com/Rapptz/discord.py) to generate a local backup of messages and files. This is not meant to be online and respond to commands like a bot, but rather be used as a CLI one-liner that can be scheduled out via `cron` or `at`, etc.

Channels are represented as HTML files, with image attachments embedded with `<img>` tags and other file types linked to with `<a>`.
All file attachments are downloaded and stored in a `/src` directory under each channel's folder.

Backups are stored in a hierarchical structure, `guild-id` -> `category-id` -> `channel-id`.
Under `channel-id` and `category-id` folders, an `index.html` file is generated with anchor links to the categories and channels, respectively, below.

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
The script expects a `key.txt` file in the same directory, containing the Discord auth token.
