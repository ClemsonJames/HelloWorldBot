import discord
from discord.ext import commands
import os

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):

        embed = discord.Embed(color=0x7ce4f7)
        embed.set_author(name='Available Commands')
        embed.add_field(name='ping', value='Pong! With latency.', inline=False)
        embed.add_field(name='when', value='Time until Hello World starts / ends.')
        embed.add_field(name='schedule', value='Hello World schedule')
        await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Help(bot))