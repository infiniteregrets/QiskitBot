import discord 
from discord.ext import commands
import asyncio 
import subprocess 
import logging
import aiohttp
from bs4 import BeautifulSoup
from arsenic import get_session, services, browsers

logger = logging.getLogger(__name__)

class DocInfo(commands.Cog):
    def __init__(self, bot):        
        self.bot = bot
        self.limit = 20
        self.render_link = 'https://qiskit.org/documentation/'  
    
    @commands.command(name = 'qdocs')
    async def qdocs(self, ctx, arg):
        if len(arg) > self.limit:
            return await ctx.send('`Query length greater than {self.limit}`')
        query_url = f'https://qiskit.org/documentation/search.html?q={arg}&check_keywords=yes&area=default#'

        service = services.Chromedriver()
        browser = browsers.Chrome()
        browser.capabilities = {
        "goog:chromeOptions": {"args": ["--headless", "--disable-gpu"]}
        }
        async with get_session(service, browser) as session:
            try:
                await session.get(query_url)
            except asyncio.TimeoutError:
                return await ctx.send('`Failed | Time Limit Exceeded`')
            else:                
                source = None
                try:
                    source = await asyncio.wait_for(session.get_page_source(), timeout=10)
                except asyncio.TimeoutError:
                    return await ctx.send('`Failed | Time Limit Exceeded`')  
                else:                    
                    soup = BeautifulSoup(source, 'html.parser')
                    summary = soup.select('.search')
                    res = []   
                    description = f''                 
                    for li in summary[0].find_all('li'):
                        link = li.find('a', href = True)                        
                        res.append(f'[`{link.contents[0]}`]({self.render_link + link["href"]})')                                                        

                    embed = discord.Embed(title = f'`Results for: {arg}`', 
                                        description = '\n'.join(res),
                                        color = 0xe8e3e3)

                    return await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(DocInfo(bot))                        