import discord
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
from aiohttp import request
from datetime import datetime
import random


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_users_id = []

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")

    @command(description="Displays the version of the bot", aliases=["info"])
    async def version(self, ctx):
        await ctx.send("I am Pybot 2.0")

    @command(description="Shows Server Info", aliases=["server", "s-i"])
    async def server_info(self, ctx):

        guild = self.bot.get_guild(773381459306217502)
        bot_user = str(self.bot.user).split("#")[0]
        owner = str(ctx.guild.owner.display_name).split("#")[0]

        embed = Embed(title=f"{guild.name}", colour=discord.Colour.from_rgb(39, 228, 255), timestamp=datetime.utcnow())

        embed.set_author(name=f"{bot_user}", icon_url=guild.icon_url)
        embed.set_thumbnail(url=guild.icon_url)

        embed.add_field(name="Owner", value=owner, inline=False)
        embed.add_field(name="Members", value=f"{len([members for members in ctx.guild.members if not members.bot])}",
                        inline=True)
        embed.add_field(name="Bots", value=f"{len([bots for bots in ctx.guild.members if bots.bot])}", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="Text Channels", value=f"{len(ctx.guild.text_channels)}", inline=True)
        embed.add_field(name="Voice Channels", value=f"{len(ctx.guild.voice_channels)}", inline=True)

        embed.set_footer(text=f"{ctx.guild.name}")

        await ctx.send(embed=embed)

    @command(description="Swears at people. (No Harsh Language)")
    async def swear(self, ctx, member: discord.Member):

        bot_users_id = []

        for bot_users in ctx.guild.members:
            if bot_users.bot:
                bot_users_id.append(bot_users.id)

        if member.id in bot_users_id:
            await ctx.send("You can't swear on bots son!")

        elif member.id == ctx.message.author.id:
            await ctx.send("Are you mad to swear yourself?")

        else:
            await ctx.send(f"{member.mention} You stupid! What do you think of yourself?")

    @command(description="Wishes the member 'Happy Birthday'")
    async def bday(self, ctx, member: discord.Member):
        await ctx.send(f"Hey {member.mention}, Happy Birthday")

    @command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

    @command(aliases=['link'])
    async def invite(self, ctx):
        server_invite = await ctx.channel.create_invite(max_age=300)
        await ctx.send(f"Here is an instant invite to your server:\n{server_invite}")

    @command()
    async def source(self, ctx):
        await ctx.send("This is my GitHub Repository:\n <https://www.github.com/NotThareesh/pybot-2.0>")

    @command()
    async def slap(self, ctx, member: discord.Member, *, reason="no reason"):

        bot_users_id = []

        for bot_users in ctx.guild.members:
            if bot_users.bot:
                bot_users_id.append(bot_users.id)

        if member in bot_users_id:
            await ctx.send("Hey, you can't slap bots!")
        else:
            await ctx.send(f"{ctx.author.display_name} slapped {member.mention} for {reason}!")

    @command()
    async def echo(self, ctx, *, message):
        await ctx.send(message)

    @command()
    async def meme(self, ctx):
        url = "https://meme-api.herokuapp.com/gimme"

        async with request("GET", url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                embed = Embed(title=data["title"], colour=discord.Colour(0x27E4FF))
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"API returned a {response.status} status.")

    @command()
    async def joke(self, ctx):
        url = "https://sv443.net/jokeapi/v2/joke/Miscellaneous,Dark,Pun?blacklistFlags=nsfw,religious,political,racist,sexist&type=twopart"

        async with request("GET", url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                embed = Embed(title=data["setup"], colour=discord.Colour(0x27E4FF))
                embed.add_field(name="\u200b", value=data["delivery"])
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"API returned a {response.status} status.")

    @command()
    async def covid(self, ctx, country=None):

        url = "https://covid-api.mmediagroup.fr/v1/cases"

        if country:
            async with request("GET", url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    embed = Embed(title=f"{country} Covid-19 Cases", colour=discord.Colour(0x27E4FF))
                    embed.set_image(url="https://assets.wam.ae/uploads/2020/07/3265571968478696090.jpg")
                    embed.add_field(name="Total Population", value="{:,}".format(data[country]["All"]["population"]))
                    embed.add_field(name="\u200b", value="\u200b")
                    embed.add_field(name="\u200b", value="\u200b")
                    embed.add_field(name="Confirmed", value="{:,}".format(data[country]["All"]["confirmed"]))
                    embed.add_field(name="Recovered", value="{:,}".format(data[country]["All"]["recovered"]))
                    embed.add_field(name="Deaths", value="{:,}".format(data[country]["All"]["deaths"]))

                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"API returned a {response.status} status.")

        else:
            url = "https://api.covid19api.com/summary"

            async with request("GET", url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    embed = Embed(title="Global Covid-19 Cases", colour=discord.Colour(0x27E4FF))
                    embed.set_image(url="https://assets.wam.ae/uploads/2020/07/3265571968478696090.jpg")
                    embed.add_field(name="New Confirmed", value="{:,}".format(data["Global"]["NewConfirmed"]))
                    embed.add_field(name="\u200b", value="\u200b")
                    embed.add_field(name="\u200b", value="\u200b")
                    embed.add_field(name="New Deaths", value="{:,}".format(data["Global"]["NewDeaths"]))
                    embed.add_field(name="New Recovered", value="{:,}".format(data["Global"]["NewRecovered"]))
                    embed.add_field(name="\u200b", value="\u200b")
                    embed.add_field(name="Total Deaths", value="{:,}".format(data["Global"]["TotalDeaths"]))
                    embed.add_field(name="Total Confirmed", value="{:,}".format(data["Global"]["TotalConfirmed"]))
                    embed.add_field(name="Total Recovered", value="{:,}".format(data["Global"]["TotalRecovered"]))

                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"API returned a {response.status} status.")

    @command()
    async def pikachu(self, ctx):

        url = "https://some-random-api.ml/img/pikachu"

        async with request("GET", url, headers={}) as response:
            if response.status == 200:
                data = await response.json()

                if data["link"][-3:] == "gif":
                    embed = Embed(title="Here's a gif of Pikachu", colour=discord.Colour(0x27E4FF))
                    embed.set_image(url=data["link"])

                    await ctx.send(embed=embed)

                else:
                    embed = Embed(title=f"Here's a picture of Pikachu", colour=discord.Colour(0x27E4FF))
                    embed.set_image(url=data["link"])

                    await ctx.send(embed=embed)

            else:
                await ctx.send(f"API returned a {response.status} status.")


def setup(bot):
    bot.add_cog(Fun(bot))
