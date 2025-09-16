import discord
from discord.ext import commands
from utils.logger import setup_logger

logger = setup_logger(__name__)

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="ping", description="Verifica a latência do bot")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latência: **{latency}ms**",
            color=discord.Color.green()
        )
        
        await ctx.send(embed=embed)
        logger.info(f"Comando ping executado por {ctx.author} - Latência: {latency}ms")
    
    @commands.hybrid_command(name="info", description="Informações sobre o bot")
    async def info(self, ctx):
        embed = discord.Embed(
            title="ℹ️ Informações do Bot",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Servidores", 
            value=len(self.bot.guilds), 
            inline=True
        )
        embed.add_field(
            name="Usuários", 
            value=len(self.bot.users), 
            inline=True
        )
        embed.add_field(
            name="Versão discord.py", 
            value=discord.__version__, 
            inline=True
        )
        
        embed.set_footer(text=f"Bot criado com Python 3 • discord.py")
        
        await ctx.send(embed=embed)
        logger.info(f"Comando info executado por {ctx.author}")
    
    @commands.hybrid_command(name="hello", description="Cumprimenta o usuário")
    async def hello(self, ctx, *, nome: str = None):
        if nome:
            mensagem = f"Olá, {nome}! 👋"
        else:
            mensagem = f"Olá, {ctx.author.mention}! 👋"
        
        embed = discord.Embed(
            title="👋 Saudações!",
            description=mensagem,
            color=discord.Color.gold()
        )
        
        await ctx.send(embed=embed)
        logger.info(f"Comando hello executado por {ctx.author}")

async def setup(bot):
    await bot.add_cog(BasicCommands(bot))