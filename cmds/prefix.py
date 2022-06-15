# Import all files from the utilities folder
from utilities import *

async def cmd(json, bot, ctx, args):

    if not ctx.author.guild_permissions.administrator:
        return await ctx.send("You do not have permission to use this command.")

    if len(args) != 1:
        return await ctx.send("only send one arg")


    server = await s.findServerInfo(bot, ctx.guild.id)

    print("server")

    with open("./utilities/serverInfo.json") as f:
        serverInfo = json.load(f)

    _id = str(server['_id'])

    oldPrefix = serverInfo[_id]['prefix']

    serverInfo[_id]['prefix'] = args[0].lower()

    with open("./utilities/serverInfo.json", "w") as outfile:
        json.dump(serverInfo, outfile, indent = 4)

    await ctx.send(f"Successfully changed {server['name']}\'s prefix from `{oldPrefix}` to `{serverInfo[_id]['prefix']}`")

    
