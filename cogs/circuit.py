import discord
from discord.ext import commands
import asyncio 
import tempfile
import subprocess
import uuid
import os
from pathlib import Path
from cogs.utils import imports
import re

policy = str(os.getcwd()) + '/sandbox/seccomp.json'
class Sandbox:
    __slots__ = ['id', 'volume']
    def __init__(self, volume):
        self.id = str(uuid.uuid4())
        self.volume = volume        
    def __enter__(self):
        subprocess.run(f'podman run --name={self.id} -v {self.volume}:/qiskit --cgroup-manager="cgroupfs"   --security-opt seccomp={policy} -i -t -d --read-only qiskitbot', shell=True, capture_output=True)
        output = subprocess.run(f'podman exec {self.id}  /bin/bash -c "cd qiskit && python3 /qiskit/circuit.py"', shell=True, capture_output=True, text=True)
        return output 
    def __exit__(self, *args, **kwargs):
        subprocess.run(f'podman container stop -l && podman container rm -l', shell=True, capture_output=True)
    def checkpoint(self):
        subprocess.run(f'podman checkpoint --cgroup-manager="cgroupfs" {self.id}', shell=True, capture_output=True)
    def restore(self):
        subprocess.run(f'podman restore --cgroup-manager="cgroupfs" {self.id}', shell=True, capture_output=True)


class Circuit(commands.Cog):
    def __init__(self, bot):        
        self.bot = bot   
        self.sandbox_dir = str(os.getcwd()) + '/sandbox'

    @commands.command(name='asciicircuit')
    async def ascii_circuit(self, ctx, *, arg):
        input = re.sub('```', "", arg).replace('py', '')
        with tempfile.TemporaryDirectory(dir=self.sandbox_dir) as session:
            circuit = Path(session) / 'circuit.py'
            with open(circuit, 'w', encoding='utf-8') as session_file:
                session_file.write("from qiskit import *")
                session_file.write(input)
                session_file.write("print(qc)")
                session_file.close()
                with Sandbox(session) as out:      
                    return await ctx.send(f'```{out.stdout}```')

    @commands.command(name='mplcircuit')
    async def circuit(self, ctx, *, arg):
        input = re.sub('```', "", arg).replace('py', '')
        with tempfile.TemporaryDirectory(dir=self.sandbox_dir) as session:
            circuit = Path(session) / 'circuit.py'
            with open(circuit, 'w', encoding='utf-8') as session_file:                
                session_file.writelines([imports.LIB_IMPORT, input, imports.CIRCUIT_SCRIPT, imports.PLOT_SCRIPT])
                print('written')
                session_file.close()
                with Sandbox(session) as out:                       
                    await ctx.send(file=discord.File(Path(session) / 'circuit.png'))

    @commands.command(name='mplplot')
    async def circuit(self, ctx, *, arg):
        input = re.sub('```', "", arg).replace('py', '')
        with tempfile.TemporaryDirectory(dir=self.sandbox_dir) as session:
            circuit = Path(session) / 'circuit.py'
            with open(circuit, 'w', encoding='utf-8') as session_file:
                session_file.writelines([imports.LIB_IMPORT, input, imports.CIRCUIT_SCRIPT, imports.PLOT_SCRIPT])
                print('written')
                session_file.close()
                with Sandbox(session) as out:
                    await ctx.send(file=discord.File(Path(session) / 'plot.png'))




def setup(bot):
    bot.add_cog(Circuit(bot)) 