import discord 
from discord.ext import commands
import asyncio 
import subprocess 
import logging
import re


logger = logging.getLogger(__name__)

class DocInfo(commands.Cog):
    def __init__(self, bot):        
        self.bot = bot
    
    @commands.command(name = 'docs')
    async def docs(self, ctx, *, arg):
        if re.match('^`[A-Za-z]{1,20}`$', arg):
            out = subprocess.run( f'echo "from qiskit import *\nhelp({arg[1:-1]})" | python3', 
                                    shell = True, text = True, capture_output = True)
            if out.returncode == 0:
                embed = discord.Embed(title = f'Info on {arg}', 
                                    description = f'```py{out.stdout}```')
                await ctx.send(embed = embed)
        else:
            embed = discord.Embed(title = 'Error', 
                                description = 'Try again with a correct class or function name and with a limit of 20 characters.')
            await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(DocInfo(bot))

