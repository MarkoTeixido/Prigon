# src/integrations/discord_bot.py
"""
🤖 Bot de Discord conversacional para Pregon
Permite a estudiantes consultar el calendario mediante comandos
"""

import discord
from discord.ext import commands
from typing import List
from datetime import datetime
from src.ai.chatbot import CalendarioChatbot
from src.models.evento import Evento
from src.config.settings import settings
from src.utils.logger import setup_logger


class PregonDiscordBot(commands.Bot):
    """
    Bot de Discord que proporciona información del calendario académico
    usando comandos y procesamiento de lenguaje natural con IA.
    """
    
    def __init__(self):
        # Configurar intents (permisos del bot)
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        
        # Inicializar bot con prefijo '!'
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None  # Usaremos nuestro propio comando de ayuda
        )
        
        self.logger = setup_logger("DiscordBot")
        self.chatbot = CalendarioChatbot()
        
        # Registrar comandos
        self._registrar_comandos()
    
    def _registrar_comandos(self):
        """Registra todos los comandos del bot"""
        
        @self.event
        async def on_ready():
            """Se ejecuta cuando el bot está listo"""
            self.logger.info(f'✅ Bot conectado como {self.user}')
            self.logger.info(f'ID: {self.user.id}')
            self.logger.info(f'Servidores: {len(self.guilds)}')
            
            # Cambiar estado del bot
            await self.change_presence(
                activity=discord.Game(name="!ayuda para comandos")
            )
        
        @self.event
        async def on_message(message):
            """Se ejecuta cuando se recibe un mensaje"""
            # Ignorar mensajes del propio bot
            if message.author == self.user:
                return
            
            # Procesar comandos
            await self.process_commands(message)
        
        @self.command(name='ayuda', aliases=['help', 'h'])
        async def ayuda(ctx):
            """Muestra la lista de comandos disponibles"""
            embed = discord.Embed(
                title="📚 Comandos de Pregon - UNViMe",
                description="Bot del calendario académico con IA",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="🤖 !pregunta <tu pregunta>",
                value="Haz una pregunta sobre el calendario usando IA\nEjemplo: `!pregunta ¿Cuándo son los exámenes?`",
                inline=False
            )
            
            embed.add_field(
                name="📅 !eventos",
                value="Muestra los eventos de la próxima semana",
                inline=False
            )
            
            embed.add_field(
                name="➕ !agregar <opción>",
                value=(
                    "Agrega eventos a tu Google Calendar\n"
                    "• `!agregar menu` - Ver opciones\n"
                    "• `!agregar 1` - Agregar evento #1\n"
                    "• `!agregar todos` - Agregar todos"
                ),
                inline=False
            )
            
            embed.add_field(
                name="🔗 !calendario",
                value="Genera links para agregar eventos individualmente",
                inline=False
            )
            
            embed.add_field(
                name="🔍 !buscar <término>",
                value="Busca eventos específicos\nEjemplo: `!buscar examen`",
                inline=False
            )
            
            embed.add_field(
                name="📆 !hoy",
                value="Muestra los eventos de hoy",
                inline=False
            )
            
            embed.add_field(
                name="ℹ️ !ayuda",
                value="Muestra este mensaje",
                inline=False
            )
            
            embed.set_footer(text="Pregon - Sistema de Notificaciones UNViMe")
            
            await ctx.send(embed=embed)
        
        @self.command(name='pregunta', aliases=['p', 'ask'])
        async def pregunta(ctx, *, consulta: str):
            """
            Responde preguntas sobre el calendario usando IA.
            
            Uso: !pregunta ¿Cuándo son los exámenes?
            """
            async with ctx.typing():  # Muestra "escribiendo..."
                try:
                    self.logger.info(f"Pregunta de {ctx.author}: {consulta}")
                    
                    # ✅ El chatbot ahora maneja el filtrado inteligente internamente
                    respuesta = await self.chatbot.responder(consulta)
                    
                    # Crear embed bonito
                    embed = discord.Embed(
                        title="🤖 Respuesta del Asistente",
                        description=respuesta,
                        color=discord.Color.green()
                    )
                    
                    embed.set_footer(
                        text=f"Pregunta de {ctx.author.name}",
                        icon_url=ctx.author.avatar.url if ctx.author.avatar else None
                    )
                    
                    await ctx.send(embed=embed)
                    
                except Exception as e:
                    self.logger.error(f"Error procesando pregunta: {e}", exc_info=True)
                    await ctx.send(
                        "❌ Lo siento, hubo un error procesando tu pregunta. "
                        "Intenta de nuevo más tarde."
                    )
        
        @self.command(name='eventos', aliases=['e', 'semana'])
        async def eventos(ctx):
            """Muestra los eventos de la próxima semana"""
            async with ctx.typing():
                try:
                    self.logger.info(f"Comando eventos de {ctx.author}")
                    
                    # Obtener eventos
                    eventos = self.chatbot.obtener_eventos_semana()
                    
                    if not eventos:
                        await ctx.send("ℹ️ No hay eventos programados para la próxima semana.")
                        return
                    
                    # Crear embed
                    embed = discord.Embed(
                        title="📅 Eventos de la Próxima Semana",
                        description=f"Total: {len(eventos)} eventos",
                        color=discord.Color.blue()
                    )
                    
                    # Agrupar por categoría
                    eventos_por_categoria = {}
                    for evento in eventos:
                        cat = evento.categoria.upper()
                        if cat not in eventos_por_categoria:
                            eventos_por_categoria[cat] = []
                        eventos_por_categoria[cat].append(evento)
                    
                    # Agregar campos por categoría
                    emojis = {
                        "ACADEMICO": "🎓",
                        "EXAMEN": "📝",
                        "FERIADO": "🎉",
                        "INSTITUCIONAL": "🏛️",
                        "RECESO": "🏖️",
                        "OTRO": "📌"
                    }
                    
                    for categoria, eventos_cat in eventos_por_categoria.items():
                        emoji = emojis.get(categoria, "📅")
                        eventos_texto = "\n".join([
                            f"• **{e.fecha.strftime('%d/%m')}** - {e.titulo}"
                            for e in eventos_cat
                        ])
                        
                        embed.add_field(
                            name=f"{emoji} {categoria}",
                            value=eventos_texto,
                            inline=False
                        )
                    
                    embed.set_footer(text="UNViMe - Calendario Académico")
                    
                    await ctx.send(embed=embed)
                    
                except Exception as e:
                    self.logger.error(f"Error obteniendo eventos: {e}", exc_info=True)
                    await ctx.send("❌ Error obteniendo eventos del calendario.")
        
        @self.command(name='buscar', aliases=['search', 'b'])
        async def buscar(ctx, *, termino: str):
            """
            Busca eventos específicos.
            
            Uso: !buscar examen
            """
            async with ctx.typing():
                try:
                    self.logger.info(f"Búsqueda de {ctx.author}: {termino}")
                    
                    # Buscar eventos
                    import asyncio
                    eventos = await self.chatbot.buscar_eventos(termino)
                    
                    if not eventos:
                        await ctx.send(f"ℹ️ No se encontraron eventos con el término: `{termino}`")
                        return
                    
                    # Crear embed
                    embed = discord.Embed(
                        title=f"🔍 Resultados: {termino}",
                        description=f"Se encontraron {len(eventos)} eventos",
                        color=discord.Color.gold()
                    )
                    
                    # Mostrar hasta 10 eventos
                    for evento in eventos[:10]:
                        fecha = evento.fecha.strftime("%d/%m/%Y")
                        embed.add_field(
                            name=f"{fecha} - {evento.categoria.upper()}",
                            value=evento.titulo,
                            inline=False
                        )
                    
                    if len(eventos) > 10:
                        embed.set_footer(text=f"Mostrando 10 de {len(eventos)} resultados")
                    
                    await ctx.send(embed=embed)
                    
                except Exception as e:
                    self.logger.error(f"Error buscando eventos: {e}", exc_info=True)
                    await ctx.send("❌ Error buscando eventos.")
        
        @self.command(name='hoy', aliases=['today'])
        async def hoy(ctx):
            """Muestra los eventos de hoy"""
            async with ctx.typing():
                try:
                    self.logger.info(f"Comando hoy de {ctx.author}")
                    
                    # Obtener eventos de hoy
                    eventos_hoy = self.chatbot.obtener_eventos_dia(datetime.now())
                    
                    if not eventos_hoy:
                        await ctx.send("ℹ️ No hay eventos programados para hoy.")
                        return
                    
                    # Crear embed
                    fecha_hoy = datetime.now().strftime("%d de %B de %Y")
                    embed = discord.Embed(
                        title=f"📆 Eventos de Hoy - {fecha_hoy}",
                        description=f"Total: {len(eventos_hoy)} eventos",
                        color=discord.Color.purple()
                    )
                    
                    for evento in eventos_hoy:
                        emoji = self._get_emoji_categoria(evento.categoria)
                        embed.add_field(
                            name=f"{emoji} {evento.categoria.upper()}",
                            value=evento.titulo,
                            inline=False
                        )
                    
                    await ctx.send(embed=embed)
                    
                except Exception as e:
                    self.logger.error(f"Error obteniendo eventos de hoy: {e}", exc_info=True)
                    await ctx.send("❌ Error obteniendo eventos de hoy.")
        
        @self.command(name='agregar', aliases=['add', 'calendar'])
        async def agregar_calendario(ctx, seleccion: str = "menu"):
            """
            Permite agregar eventos seleccionados a Google Calendar.
            
            Uso: 
            !agregar menu → Muestra menú de selección
            !agregar 1 → Agrega evento #1
            !agregar todos → Agrega todos los eventos
            """
            async with ctx.typing():
                try:
                    from src.integrations.calendar_manager import CalendarManager
                    
                    manager = CalendarManager()
                    
                    # Obtener eventos de la semana
                    eventos = self.chatbot.obtener_eventos_semana()
                    
                    if not eventos:
                        await ctx.send("ℹ️ No hay eventos próximos para agregar.")
                        return
                    
                    # Caso 1: Mostrar menú
                    if seleccion.lower() == "menu":
                        embed_data = manager.generar_embed_discord_seleccionable(eventos)
                        
                        import discord
                        embed = discord.Embed(
                            title=embed_data['title'],
                            description=embed_data['description'],
                            color=embed_data['color']
                        )
                        
                        for field in embed_data['fields']:
                            embed.add_field(**field)
                        
                        embed.set_footer(text="Usa !agregar <número> para agregar un evento")
                        
                        await ctx.send(embed=embed)
                    
                    # Caso 2: Agregar todos
                    elif seleccion.lower() == "todos" or seleccion.lower() == "all":
                        await ctx.send("📅 Agregando todos los eventos a Google Calendar...")
                        
                        resultado = manager.calendar_service.agregar_multiples_eventos(eventos)
                        
                        if resultado['exitosos'] > 0:
                            await ctx.send(
                                f"✅ Se agregaron {resultado['exitosos']}/{resultado['total']} eventos a tu calendario.\n"
                                f"🔗 Revisa tu Google Calendar"
                            )
                        else:
                            await ctx.send("❌ No se pudieron agregar los eventos. Verifica la configuración.")
                    
                    # Caso 3: Agregar evento específico por número
                    elif seleccion.isdigit():
                        numero = int(seleccion)
                        
                        if 1 <= numero <= len(eventos):
                            evento = eventos[numero - 1]
                            
                            await ctx.send(f"📅 Agregando: {evento.titulo}...")
                            
                            resultado = manager.calendar_service.agregar_evento(evento)
                            
                            if resultado:
                                await ctx.send(
                                    f"✅ Evento agregado a tu calendario!\n"
                                    f"📆 {resultado['evento']}\n"
                                    f"🔗 {resultado['link']}"
                                )
                            else:
                                await ctx.send("❌ No se pudo agregar el evento.")
                        else:
                            await ctx.send(f"❌ Número inválido. Usa un número entre 1 y {len(eventos)}")
                    
                    else:
                        await ctx.send(
                            "❌ Uso incorrecto. Ejemplos:\n"
                            "• `!agregar menu` - Muestra opciones\n"
                            "• `!agregar 1` - Agrega evento #1\n"
                            "• `!agregar todos` - Agrega todos"
                        )
                        
                except Exception as e:
                    self.logger.error(f"Error en comando agregar: {e}", exc_info=True)
                    await ctx.send("❌ Error procesando comando.")

        @self.command(name='calendario', aliases=['cal'])
        async def calendario_links(ctx):
            """
            Genera links para agregar eventos individualmente.
            
            Uso: !calendario
            """
            async with ctx.typing():
                try:
                    from src.integrations.calendar_manager import CalendarManager
                    
                    manager = CalendarManager()
                    eventos = self.chatbot.obtener_eventos_semana()
                    
                    if not eventos:
                        await ctx.send("ℹ️ No hay eventos próximos.")
                        return
                    
                    opciones = manager.generar_opciones_seleccion(eventos)
                    
                    # ✅ Función helper para emojis
                    def get_emoji(categoria: str) -> str:
                        emojis = {
                            "academico": "🎓",
                            "examen": "📝",
                            "feriado": "🎉",
                            "institucional": "🏛️",
                            "receso": "🏖️",
                            "otro": "📌"
                        }
                        return emojis.get(categoria.lower(), "📅")
                    
                    import discord
                    embed = discord.Embed(
                        title="📅 Links para Agregar a Google Calendar",
                        description="Click en los links para agregar eventos individuales:",
                        color=discord.Color.blue()
                    )
                    
                    for opcion in opciones['eventos']:
                        fecha = opcion['evento'].fecha.strftime("%d/%m")
                        emoji = get_emoji(opcion['categoria'])
                        
                        embed.add_field(
                            name=f"{emoji} {fecha} - {opcion['titulo']}",
                            value=f"[➕ Agregar a Calendar]({opcion['link']})",
                            inline=False
                        )
                    
                    embed.set_footer(text="Click en los links para agregar a tu calendario")
                    
                    await ctx.send(embed=embed)
                    
                except Exception as e:
                    self.logger.error(f"Error generando links: {e}", exc_info=True)
                    await ctx.send("❌ Error generando links de calendario.")


def run_discord_bot():
    """
    Función helper para iniciar el bot de Discord.
    """
    logger = setup_logger("DiscordBotRunner")
    
    if not settings.discord_bot_token:
        logger.error("❌ DISCORD_BOT_TOKEN no está configurado en .env")
        logger.error("Obtén tu token en: https://discord.com/developers/applications")
        return
    
    try:
        logger.info("🚀 Iniciando bot de Discord...")
        bot = PregonDiscordBot()
        bot.run(settings.discord_bot_token)
    except Exception as e:
        logger.error(f"❌ Error iniciando bot: {e}", exc_info=True)