import discord

whitelist = [<DEV USER ID HERE AS INT>]

blacklist = [<USER ID HERE AS INT>]

devmode = False # True/False, enables/disables devmode. Changes default prefix and will eventually do more

defaultPrefix = "!!"
devPrefix = "??"

logChannelId = <CHANNEL ID HERE AS INT>
failCmdChannelId = <CHANNEL ID HERE AS INT>

# Playing -> activity = discord.Game(name="!help")
# Streaming -> activity = discord.Streaming(name="!help", url="twitch_url_here")
# Listening -> activity = discord.Activity(type=discord.ActivityType.listening, name="!help")
# Watching -> activity = discord.Activity(type=discord.ActivityType.watching, name="!help")
activity = discord.Game(
    name = "use " + defaultPrefix + " for help"
)