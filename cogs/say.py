import discord
from discord.ext import commands


class Say(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Commands
    @commands.command()
    async def say(self, ctx, channel, *, msg):
        guild = self.bot.get_guild(781233594759643157)
        channel = discord.utils.get(guild.channels, name=channel)
        await channel.send(msg)


# Connect cog to bot
def setup(bot):
    bot.add_cog(Say(bot))