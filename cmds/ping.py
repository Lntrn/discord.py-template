async def cmd(bot, ctx):
    await ctx.send(f"Pong! `{round(bot.latency * 1000)}ms`")