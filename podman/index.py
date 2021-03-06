import discord 
from discord.ext import commands
import config
import logging
import logging.config
from os import listdir
import asyncio

extension_blacklist = ['__init__.py', 'qdocs.py']

class Qiskit(commands.Bot):
    def __init__(self):                     
        intents = discord.Intents( 
        guilds=True, 
        members=True, 
        messages=True, 
        reactions=True, 
        presences=True
        )
        allowed_mentions = discord.AllowedMentions(roles=False, users=True, everyone=False)        

        super().__init__(command_prefix = commands.when_mentioned_or(config.PREFIX),
                         case_insensitive = True,
                         self_bot = False,
                         description = "IBMQiskit Discord Bot",
                         allowed_mentions = allowed_mentions,
                         intents = intents, 
                         owner_id = 624458069220524034
        )
        

        logging.basicConfig(filename='loginfo.log', 
                            filemode='w', 
                            level=logging.INFO)

        self.logger = logging.getLogger(__name__)

        def add_cog(self, extension: commands.Cog) -> None:        
            self.logger.info(f"Loading extension: {extension.qualified_name}")
            super().add_cog(extension)

        for extension in filter(lambda x: x.endswith(".py") and x not in extension_blacklist, listdir("cogs/")):
            try:
                self.load_extension(f"cogs.{extension[:-3]}")
                self.logger.info(f'{extension} loaded')
            except Exception as e:                
                self.logger.exception(f'Failed to load extension {extension} | Error {e}')

    async def on_ready(self) -> None:    
        self.logger.info(f'Application logged in  {self.user.name} | ID {self.user.id} | Version - d.py version: {discord.__version__}')          
    
    async def on_resumed(self) -> None:
        self.logger.info(f'Reconnected {self.user.id} ({self.user.name})')
    
          


   



