import discord
from discord.ext import commands
import asyncio
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger()

class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        super().__init__(
            command_prefix=settings.PREFIX,
            intents=intents,
            help_command=None
        )
    
    async def update_guild_commands(self, guild=None):
      """Sincroniza os comandos com um servidor específico ou globalmente"""
      try:
        if guild:
          self.tree.copy_global_to(guild=guild)
          await self.tree.sync(guild=guild)
          logger.info(f"Comandos sincronizados para o servidor {guild.name} (ID: {guild.id})")
        else:
          await self.tree.sync()
          logger.info("Comandos globais sincronizados com sucesso")
      except Exception as e:
        if guild:
          logger.error(f"Erro ao sincronizar comandos no servidor {guild.name}: {e}")
        else:
          logger.error(f"Erro ao sincronizar comandos globais: {e}")

    async def setup_hook(self):
      try:
        await self.load_extension('cogs.basic_commands')
        await self.load_extension('cogs.voice_commands')
        logger.info("Cogs carregados com sucesso")
          
      except Exception as e:
        logger.error(f"Erro ao carregar cogs: {e}")
    
    async def on_ready(self):
      logger.info(f'{self.user} está online!')
      logger.info(f'Conectado a {len(self.guilds)} servidor(es)')
      
      for guild in self.guilds:
        logger.info(f"Servidor: {guild.name} (ID: {guild.id}) - {guild.member_count} membros")
        await self.update_guild_commands(guild)

        
        activity = discord.Activity(
            type=discord.ActivityType.watching, 
            name=f"{len(self.guilds)} servidores"
        )
        await self.change_presence(activity=activity)
    
    async def on_guild_join(self, guild):
        """Evento chamado quando o bot entra em um novo servidor"""
        logger.info(f"Bot adicionado ao servidor: {guild.name} (ID: {guild.id})")
        
        try:
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            logger.info(f"Comandos sincronizados no novo servidor: {guild.name}")
        except Exception as e:
            logger.error(f"Erro ao sincronizar comandos no novo servidor {guild.name}: {e}")
        
        activity = discord.Activity(
            type=discord.ActivityType.watching, 
            name=f"{len(self.guilds)} servidores"
        )
        await self.change_presence(activity=activity)
    
    async def on_guild_remove(self, guild):
        """Evento chamado quando o bot é removido de um servidor"""
        logger.info(f"Bot removido do servidor: {guild.name} (ID: {guild.id})")
        
        activity = discord.Activity(
            type=discord.ActivityType.watching, 
            name=f"{len(self.guilds)} servidores"
        )
        await self.change_presence(activity=activity)
    
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="❌ Erro",
                description="Argumentos obrigatórios não fornecidos.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        logger.error(f"Erro no comando {ctx.command}: {error}")
        
        embed = discord.Embed(
            title="❌ Erro Inesperado",
            description="Ocorreu um erro inesperado. Tente novamente.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

async def main():
    try:
        settings.validate()
        bot = DiscordBot()
        async with bot:
            await bot.start(settings.DISCORD_TOKEN)
    except ValueError as e:
        logger.error(f"Erro de configuração: {e}")
    except Exception as e:
        logger.error(f"Erro ao iniciar o bot: {e}")

if __name__ == "__main__":
    asyncio.run(main())