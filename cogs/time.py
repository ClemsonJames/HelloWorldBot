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

start = dt.fromtimestamp(1612000800, tz = est)
end = dt.fromtimestamp(1612101600, tz = est) 

orl = partial(dt.now, tz = est)


sched = {
    30: [
        ('10:00 am', 'Opening Ceremony', ''),
        ('10:30 am', 'Hacking Starts!!!', ''),
        ('10:30 am', 'Boss of the SOC (Splunk)', ''),
        ('12:30 am', 'Azure Skills Workshop', ''),
        ('1:00 pm', 'Recruiting Sesssion (Softdocs)', ''),
        ('1:30 pm', 'Trivia', ''),
        ('2:00 pm', 'Recruiting Sesssion (LPL and Capgemini)', ''),
        ('2:30 pm', 'Bob Ross', ''),
        ('3:00 pm', 'Recruiting Sesssion (GLS)', ''),
        ('3:30 pm', 'Boss of the NOC (Splunk)', ''),
        ('4:00 pm', 'Among Us', ''),
        ('4:30 am', 'Student Journey to Microsoft Q/A', ''),
        ('5:00 pm', 'Air Force Cybersecurity (MLH)', ''),
        ('5:30 pm', 'Recruiting Sesssion (LPL and ASH)', ''),
        ('6:00 pm', 'Scavenger Hunt', ''),
        ('7:00 pm', 'Game Tournament ', ''),
        ('8:00 pm', 'Jackbox', ''),
    ],
        31: [
        ('10:00 am', 'DevPost Submissions Due', ''),
        ('10:30 am', 'Hacking Ends!!!', ''),
        ('11:00 am', 'Live Demos and Judging', ''),
        ('1:30 pm', 'Closing Ceremony', ''),
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
            breakdown = "CUhackit 2021 is over :(("
        else:
            breakdown = "CUhackit 2021 " \
                + ("begins " if start > orl() else "ends ") \
                + "in " + time_left(event) + " bb"

        await ctx.send(breakdown)

    @commands.command()
    async def schedule(self, ctx):
        embeds = []

        for day, events in sched.items():
            if day >= orl().day:

                embed = discord.Embed(title = 'CUhackit 2021 Schedule :scroll:',
                                      color = 0x7ce4f7)

                for num, event in enumerate(events):
                    event_time, event_name, link = event
                    left = dt.strptime(f"2021 Jan {day} {event_time}", "%Y %b %d %I:%M %p").replace(tzinfo=est)
                    if (left > orl()):
                        embed.add_field(name=f"{num + 1}. {event_name}: Jan {day}, {event_time}",
                                    value=(f"in {time_left(left)}" + (f", [**link**]({link})" if link else '')),
                                    inline=False)

                embeds.append(embed)

        await paginate_embed(self.bot, ctx.channel, embeds)

def setup(bot):
    bot.add_cog(Times(bot))