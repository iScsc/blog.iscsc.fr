---
title: "Making a Discord bot to notify of new articles"
summary: "Simple tutorial to Discord bots using `discord.py`"
date: 2022-12-07T00:31:02-02:00
lastUpdate: 2022-12-07T00:31:02-02:00
tags: ["python","discord","bot"]
author: gbrivady
draft: false
---

Warm welcome to the `iSCSC Blog Bot` on the Discord server!

`iSCSC Blog Bot` is a 
Discord bot built using the `discord.py` API wrapper ([documentation here](https://discordpy.readthedocs.io/en/stable/)).
Its only aim is to send a message on the `#📡•serveur`  channel everytime someone posts a new blog article (such as this one 👀). 

If you want to have a look at the source code, maybe to build your very own Discord bot, [have a look at the GitHub repo](https://github.com/iScsc/iscsc.fr-blog-notify)!

# How does it work?

Every 10 minutes - configurable in the code - the bot sends a request to the website API (https://iscsc.fr/api/articles), then compare it to a cached version, and sends a message for every new article detected. The application is split in two parts: one that caches and read the API requests, and the bot in itself.

## DIY at home
### Sending requests using the `requests` module

Sending and reading requests in python is not very hard, so I'm just going to gloss over it.

```python
import requests

r = requests.get('url')
dic = r.json()
```

Sends a request to a given url, saves the answer to `r` and save it as a json dictionnary. You can do a lot of other things - such as checking for errors - by accessing specific attributes of `r`. For more information, look at the [documentation](https://requests.readthedocs.io/en/latest/).
If you know your way around a dictionnary, and look at the json in your browser, you should be able to do pretty much anything you want.

### A simple message-sending Discord bot
To create a bot, we are going to look at the `ext` module of `discord.py`, and do something a bit like that:
```python
import discord
from discord.ext import commands

intent = discord.Intents.default()
intent.message_content = True

bot = commands.Bot(command_prefix = '!', intents = intent)
```
Pretty simple right? But what is a `discord.Intents`? Glad you asked. 

`Intents` are basically "permissions" for your Discord bot. The default set of permissions allows you to have pretty much every permission, but reading messages and their content, and seeing connected members. If you want to be able to respond to commands, you are going to want to turn that on.
The full documentation for the class is [here](https://discordpy.readthedocs.io/en/stable/api.html?highlight=intents#discord.Intents) if you want to have a look at it.

#### Sending messages using the bot

##### Automatically
To send a message in a **specific** channel, you are going to need the id of that channel. To get the id of a text channel, turn on developer mode in your Discord app (Settings > Advanced), right click on a text channel in the list of channels, and simply copy the id. 

We are first going to "connect" the bot to the channel, using the `fetch_channel` method of our bot, and then send a message using the `send` method of our channel, so something like this:

```python
from discord.ext import tasks

@tasks.loop(minutes=REFRESH_TIME)
async def auto_send_message()
    channel = await bot.fetch_channel(CHANNEL_ID)
    channel.send("Message")
```
Here, the `@tasks.loop(minutes=REFRESH_TIME)` decorator makes our function a looping task for our bot, repeating it every `REFRESH_TIME` minutes - you can also set this to `seconds` or `hour` if you wish to do so.

Finally, to make it so your bot starts its task at startup, add the following function to your code:
```python
@bot.event
async def on_ready():
    auto_send_message.start()
```

And now you just need to start your bot - see the next section.

##### Responding to a command

Responding to a command is even easier: you can directly get the channel, without needing to have its id:

```python
@bot.command()
def respond(ctx):
    await ctx.message.channel.send("Response")
```
This code will make it so your bot responds with `Response` everytime someones types `!repond` in any Discord channel your bot can see.

All the information is already in the `ctx` argument of the function in this case.

#### Starting the bot

To get your bot running, you are going need a bot token. Find more information about how to get one on the [Discord Developer Portal](https://discord.com/developers/docs/intro).

Add the following lines to **at the end** of your code:

```python
if __name__ == "__main__":
    try:       
        bot.run('your_bot_token_goes_here')
    except discord.errors.LoginFailure:
        print("Invalid Discord token!")
        exit(1)
```

And you are set to go! Just add your favorite Discord server, and ~spam~ have fun using your bot!

If you want to do more complicated stuff, but do not know where to start - have a look at the [documentation for `discord.py`](https://discordpy.readthedocs.io/en/stable/).
