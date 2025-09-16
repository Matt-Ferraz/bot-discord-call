import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD_ID = None
    PREFIX = '!'
    
    def __init__(self):
        guild_id_str = os.getenv('GUILD_ID')
        if guild_id_str and guild_id_str != 'seu_guild_id_aqui':
            try:
                self.GUILD_ID = int(guild_id_str)
            except ValueError:
                self.GUILD_ID = None
    
    @classmethod
    def validate(cls):
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN não encontrado no arquivo .env")

settings = Settings()