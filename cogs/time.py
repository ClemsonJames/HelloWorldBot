'''
Credit for this code goes to Aadi, from VandyHacks!
Also belle from KnightHacks
https://github.com/aadibajpai
https://github.com/lienne
'''


from datetime import timedelta, timezone as tz, datetime as dt
from functools import partial

from utils import paginate_embed

import discord
from discord.ext import commands

#est is 4hrs ahead of utc
est = tz(timedelta(hours = -4))

start = dt.fromtimestamp(1602936000, tz = est) # 8am Oct 17th 2020
end = dt.fromtimestamp(1602979200, tz = est) # 8pm Oct 17th 2020

orl = partial(dt.now, tz = est)


sched = {
    17: [
        ('8:00 am', 'Opening Ceremony', ''),
        ('8:30 am', 'Hacking Starts!!! (Team Formation)', ''),
        ('9:00 am', 'Idea jam workshop', ''),
        ('10:00 am', 'Activity 1: Jackbox', ''),
        ('11:30 am', 'Activity 2: Trivia/Kahoot', ''),
        ('1:00 pm', 'Activity 3: Panel Discussion', ''),
        ('2:30 pm', 'Activity 4: Scavenger Hunt Reveal', ''),
        ('4:00 pm', 'Activity 5: Yoga', ''),
        ('6:30 pm', 'Hacking Ends!!!', ''),
        ('7:00 pm', 'Demos and Judging', ''),
        ('8:00 pm', 'Award', ''),
        ('8:30 pm', 'Closing Ceremony', ''),
        ('9:00 pm', 'Debrief', ''),
    ]
}

def time_left(event):
    diff = event - orl()
    d = diff.days
    h, m = divmod(diff.seconds, 3600)
    m, s = divmod(m, 60)

    return (f"{d} day{'s' * bool(d - 1)}, " if d else "") \
           + (f"{h} hour{'s' * bool(h - 1)}, " if h else "") \
           + (f"{m} minute{'s' * bool(m - 1)} and " if m else "") \
           + f"{s} second{'s' * bool(s - 1)}"


class Times(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def when(self, ctx):
        if start > orl():
            event = start
        else:
            event = end

        if orl() > end:
            breakdown = "Hello World is over :(("
        else:
            breakdown = "Hello World " \
                + ("begins " if start > orl() else "ends ") \
                + "in " + time_left(event) + " bb"

        await ctx.send(breakdown)

    @commands.command()
    async def schedule(self, ctx):
        embeds = []

        for day, events in sched.items():
            if day >= orl().day:

                embed = discord.Embed(title = 'Hello World 2020 Schedule :scroll:',
                                      color = 0x7ce4f7)

                for num, event in enumerate(events):
                    event_time, event_name, link = event
                    left = dt.strptime(f"2020 Oct {day} {event_time}", "%Y %b %d %I:%M %p").replace(tzinfo=est)
                    if (left > orl()):
                        embed.add_field(name=f"{num + 1}. {event_name}",
                                    value=(f"in {time_left(left)}" + (f", [**link**]({link})" if link else '')),
                                    inline=False)

                embeds.append(embed)

        await paginate_embed(self.bot, ctx.channel, embeds)

def setup(bot):
    bot.add_cog(Times(bot))