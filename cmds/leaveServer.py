# Import all files from the utilities folder
from utilities import *
async def cmd(discord, json, bot, ctx, args):

    if ctx.author.id not in config.whitelist:
        return await ctx.send("Only a bot dev can run this command!")

    server = await s.findServerInfo(bot, args[0])
    _id = str(server['_id'])

    guild = bot.get_guild(server['_id'])

    print(guild)

    if guild == None:
        return await ctx.send(f"Could not find a guild from id `{server['_id']}`")
    await guild.leave()
    await ctx.send(f"Successfully left {server['name']}")

    with open("./utilities/serverInfo.json") as f:
        serverInfo = json.load(f)

    del serverInfo[_id]
    with open("./utilities/serverInfo.json", "w") as outfile:
        json.dump(serverInfo, outfile, indent = 4)

    print(f"Successfully removed {server['name']} from {outfile}")
    