import discord 
from discord.ext import commands
import asyncio 
import aiohttp
import json
import subprocess 
import logging



logger = logging.getLogger(__name__)

class Queries(commands.Cog):
    def __init__(self, bot):        
        self.bot = bot
        self.order = ['desc', 'asc']
        self.sort = ['activity', 'hot', 'creation', 'votes', 'month', 'week']
    
    @commands.command(name = 'query')
    async def query(self, ctx, *args):
        if len(args) != 3:
            return await ctx.send('`Invalid number of arguments`')
        elif len(args[0]) > 100:
            return await ctx.send('`Shorten your query`')                    
        elif args[1] not in self.sort:
            return await ctx.send('`Invalid sort argument`')
        elif args[2] not in self.order:
            return await ctx.send('`Invalid order argument`')

        query_url = f'https://api.stackexchange.com/2.2/search/advanced?page=1&pagesize=5&order={args[2]}&sort={args[1]}&title={args[0]}&site=quantumcomputing'
        async with aiohttp.ClientSession() as client_session:
            async with client_session.get(query_url) as response:
                if response.status != 200:
                    return await ctx.send(f'An error occurred | status code: {response.status}')
                else:
                    json_resp = json.loads(await response.text())

                    embed = discord.Embed(title = f'`Results for: {args[0]}`')
                    for i in range(5):
                        embed.add_field(name=f'`Score` {json_resp["items"][i]["score"]} | `View Count` {json_resp["items"][i]["view_count"]} | `Answer Count` {json_resp["items"][i]["answer_count"]}', 
                                        value = f'[{json_resp["items"][i]["title"]}]({json_resp["items"][i]["link"]})', 
                                        inline=False)                        
                    embed.set_thumbnail(url = 'https://imgur.com/uJEVozR')
                    await ctx.send(embed = embed)




def setup(bot):
    bot.add_cog(Queries(bot))        