import docker 
import os
import uuid
import re
import discord
from discord.ext import commands
import tempfile
from .utils import scripts
from .utils.sandbox import Sandbox
from pathlib import Path

docker_client = docker.from_env()

class User():
    def __init__(self):
        self.id = str(uuid.uuid4())


class Circuit(commands.Cog):
    def __init__(self, bot):        
        self.bot = bot
        self.pattern = re.compile('^(```)(py|python|\n)(?P<code>[\x00-\x7F]+)(```)$')
        self.error_messages = ['`Error while parsing input. Make sure your code is formatted properly.`', 
                                'Error | missing build_state() function']
        self.sandbox_dir = str(os.getcwd()) + '/sandbox'
        self.image = 'qiskitsandbox'
        self.command = 'timeout 100 /bin/bash -c "cd qiskit && python3 /qiskit/circuit.py"'
        self.volume = None
                                

    @commands.cooldown(3, 30, commands.BucketType.user)
    @commands.command(name = 'asciicircuit')   
    async def circuit(self, ctx, *, arg):
        code = None
        if not self.pattern.match(arg):
           return await ctx.reply(f'{self.error_message[0]}')
        try:
            code = re.search(self.pattern, arg).group('code')
        except AttributeError:
            return await ctx.reply(f'{self.error_messages[0]}')
        if not code.strip().startswith('def build_state():'):            
            return await ctx.reply(f'`{self.error_messages[1]}`\n{code}')
        
        with tempfile.TemporaryDirectory(dir=self.sandbox_dir) as session:
            circuit = Path(session) / 'circuit.py'
            with open(circuit, 'w', encoding='utf-8') as session_file:                
                session_file.writelines([scripts.LIB_IMPORT, 
                                        code, 
                                        scripts.ASCII_CIRCUIT_SCRIPT])
                session_file.close()
                self.volume={session: 
                                {'bind': '/qiskit/', 
                                'mode': 'rw'}
                            }
                sandbox=Sandbox(self.image, self.command, self.volume)
                out = sandbox.run().decode("utf-8") 
                return await ctx.reply(f'```{out}```')
        
    # @circuit.error
    # async def on_command_error(self, ctx, exception):
    #     if isinstance(exception, commands.CommandOnCooldown):
    #         embed = discord.Embed(title="`You are on a cooldown`", 
    #                             description=f"`Please try again in {int(exception.retry_after)} seconds`")
    #     await ctx.reply(embed=embed, mention_author=True)
    



def setup(bot):
    bot.add_cog(Circuit(bot))
