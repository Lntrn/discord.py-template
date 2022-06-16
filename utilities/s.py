import json
import random

async def randomColour():
    colours = [0x4dff58, 0x9740dd, 0x3455f9, 0xec7a22, 0x5dfdf3, 0xff0000, 0x3a2848, 0x3f798d, 0x86a15e, 0xabff66, 0xfbff14, 0x9fa073, 0x235333, 0x010698, 0xff00d4, 0x8c184c, 0x000000, 0x5865F2, 0x2f3136]
    return random.choice(colours)

async def findServerInfo(bot, _id):

    with open("./utilities/serverInfo.json") as f:
        serverInfo = json.load(f)
        
    return serverInfo.get(str(_id))

async def logCmd(discord, config, ctx, bot, args):
    argsStr = " ".join(args)

    if ctx.guild == None:
        guildmsg = f"**Guild Name**: {ctx.guild}"
    else:
        guildmsg = f"**Guild Name**: {ctx.guild}\n**Guild ID**: {ctx.guild.id}"

    

    embed = discord.Embed(
        color = 0x2AF4C8,
        title = f"Command Used",
        description = f"**Command Used**: `{ctx.command}`\n**Args**:\n> {argsStr}\n**User**: <@{ctx.author.id}\n{guildmsg}\n**Channel**: <#{ctx.channel.id}>"
    )

    await bot.get_channel(config.logChannelId).send(embed = embed)

async def cmdFail(discord, config, ctx, bot, args):
    argsStr = " ".join(args)

    embed = discord.Embed(
        color = 0xFF0000,
        title = f"Command Failed!",
        description = f"Command Used**: `{ctx.command}`\nArgs:\n> {argsStr}\nUser: <@{ctx.author.id}>\nServer: {ctx.guild}\nChannel: <#{ctx.channel.id}>\nReason for failuren> Coming soon.."
    )

    await bot.get_channel(config.failCmdChannelId).send(embed = embed)


async def processArgs(args):
    joint = " ".join(args)
    split = joint.split(",")
    data = []

    for x in split:
        d = {
            "content": x.strip(),
            "exact": False
        }
        data.append(d)

    return data