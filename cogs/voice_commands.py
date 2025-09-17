import discord
from discord.ext import commands
from utils.logger import setup_logger

logger = setup_logger(__name__)

class VoiceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="join", description="Bot entra no canal de voz do usuário")
    async def join_voice(self, ctx):
        # Verificar se o usuário está em um canal de voz
        if not ctx.author.voice:
            embed = discord.Embed(
                title="❌ Erro",
                description="Você precisa estar em um canal de voz para usar este comando!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # Verificar se o bot já está conectado a algum canal de voz no servidor
        if ctx.voice_client:
            # Se já estiver conectado, mover para o canal do usuário
            if ctx.voice_client.channel == ctx.author.voice.channel:
                embed = discord.Embed(
                    title="ℹ️ Informação",
                    description=f"Já estou conectado ao canal **{ctx.author.voice.channel.name}**!",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
                return
            else:
                # Mover para o novo canal
                await ctx.voice_client.move_to(ctx.author.voice.channel)
                embed = discord.Embed(
                    title="🔄 Movido",
                    description=f"Movido para o canal **{ctx.author.voice.channel.name}**!",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
                logger.info(f"Bot movido para o canal {ctx.author.voice.channel.name} por {ctx.author}")
                return
        
        # Conectar ao canal de voz do usuário
        try:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()
            
            embed = discord.Embed(
                title="🎵 Conectado",
                description=f"Conectado ao canal **{voice_channel.name}**!",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            logger.info(f"Bot conectado ao canal {voice_channel.name} por {ctx.author}")
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro",
                description="Não foi possível conectar ao canal de voz. Verifique as permissões do bot.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            logger.error(f"Erro ao conectar ao canal de voz: {e}")
    
    @commands.hybrid_command(name="leave", description="Bot sai do canal de voz")
    async def leave_voice(self, ctx):
        # Verificar se o bot está conectado a um canal de voz
        if not ctx.voice_client:
            embed = discord.Embed(
                title="❌ Erro",
                description="Não estou conectado a nenhum canal de voz!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # Verificar se o usuário está no mesmo canal que o bot
        if ctx.author.voice and ctx.author.voice.channel == ctx.voice_client.channel:
            channel_name = ctx.voice_client.channel.name
            await ctx.voice_client.disconnect()
            
            embed = discord.Embed(
                title="👋 Desconectado",
                description=f"Desconectado do canal **{channel_name}**!",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            logger.info(f"Bot desconectado do canal {channel_name} por {ctx.author}")
            
        else:
            embed = discord.Embed(
                title="❌ Erro",
                description="Você precisa estar no mesmo canal de voz que eu para me desconectar!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name="voice_info", description="Informações sobre a conexão de voz")
    async def voice_info(self, ctx):
        if not ctx.voice_client:
            embed = discord.Embed(
                title="🎵 Status de Voz",
                description="Não estou conectado a nenhum canal de voz.",
                color=discord.Color.blue()
            )
        else:
            voice_channel = ctx.voice_client.channel
            members_in_channel = len([m for m in voice_channel.members if not m.bot])
            
            embed = discord.Embed(
                title="🎵 Status de Voz",
                color=discord.Color.green()
            )
            embed.add_field(
                name="Canal Conectado",
                value=voice_channel.name,
                inline=True
            )
            embed.add_field(
                name="Usuários no Canal",
                value=f"{members_in_channel} usuários",
                inline=True
            )
            embed.add_field(
                name="Latência de Voz",
                value=f"{round(ctx.voice_client.latency * 1000)}ms" if hasattr(ctx.voice_client, 'latency') else "N/A",
                inline=True
            )
        
        await ctx.send(embed=embed)
        logger.info(f"Comando voice_info executado por {ctx.author}")
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Evento chamado quando há mudanças no estado de voz dos membros"""
        # Se o bot foi desconectado do canal
        if member == self.bot.user and before.channel and not after.channel:
            logger.info(f"Bot foi desconectado do canal {before.channel.name}")
        
        # Verificar se o bot está sozinho no canal e desconectar automaticamente
        if before.channel and self.bot.user in before.channel.members:
            # Contar membros que não são bots
            human_members = [m for m in before.channel.members if not m.bot]
            
            # Se não há mais usuários humanos no canal, desconectar
            if len(human_members) == 0:
                for voice_client in self.bot.voice_clients:
                    if voice_client.channel == before.channel:
                        await voice_client.disconnect()
                        logger.info(f"Bot desconectado automaticamente do canal {before.channel.name} (canal vazio)")
                        break

async def setup(bot):
    await bot.add_cog(VoiceCommands(bot))