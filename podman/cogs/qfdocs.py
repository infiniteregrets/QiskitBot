import discord 
from discord.ext import commands
import asyncio 
import subprocess 
import logging
import aiohttp
from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession
import nest_asyncio

nest_asyncio.apply()

logger = logging.getLogger(__name__)

class QDocInfo(commands.Cog):
    def __init__(self, bot):        
        self.bot = bot
        self.render_link = 'https://qiskit.org/documentation/'  
        self.title = ''
        self.res = []

    @commands.command(name = 'qfdocs')
    async def qfdocs(self, ctx, arg):
        query_url = f'https://qiskit.org/documentation/search.html?q={arg}&check_keywords=yes&area=default#'
        try:
            session = AsyncHTMLSession()
            response = await session.get(query_url)
        except:
            return await ctx.send('`Failed to Establish Connection.`')

        else:
            await response.html.arender(sleep=7)
            soup = BeautifulSoup(response.html.html, "html.parser")
            summary = soup.select('.search')
                #return await ctx.send('`Request Timed Out`')            

        description = f''                 
        for li in summary[0].find_all('li')[0:10]:
            link = li.find('a', href = True)                        
            self.res.append(f'[`{link.contents[0]}`]({self.render_link + link["href"]})') 
        
        if self.res == []:            
            self.title = '`No Results Found`'
        else:
            self.title = f'`Results for: {arg}`'

        embed = discord.Embed(title = self.title, 
                            description = '\n'.join(self.res),
                            color = 0xe8e3e3)

        return await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(QDocInfo(bot))                        