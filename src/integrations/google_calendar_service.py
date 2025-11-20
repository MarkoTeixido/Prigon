# src/integrations/google_calendar_service.py
"""
📅 Servicio de Google Calendar
Permite agregar eventos al calendario de los usuarios
"""

import os
import pickle
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.models.evento import Evento
from src.config.settings import settings
from src.utils.logger import setup_logger


class GoogleCalendarService:
    """
    Servicio para interactuar con Google Calendar API.
    Permite agregar eventos automáticamente al calendario del usuario.
    """
    
    # Scopes necesarios para Calendar
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    def __init__(self):
        self.logger = setup_logger("GoogleCalendar")
        self.creds = None
        self.service = None
        
        # Rutas de credenciales
        self.credentials_path = settings.google_credentials_path
        self.token_path = settings.google_token_path
        
        # Inicializar servicio
        self._authenticate()
    
    def _authenticate(self):
        """
        Autentica con Google Calendar usando OAuth 2.0.
        
        La primera vez abre un navegador para autorizar.
        Luego guarda el token para usos futuros.
        """
        # Verificar que exista el archivo de credenciales
        if not os.path.exists(self.credentials_path):
            self.logger.error(f"❌ Archivo de credenciales no encontrado: {self.credentials_path}")
            self.logger.error("Descarga las credenciales desde Google Cloud Console")
            return
        
        # Cargar token guardado si existe
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                self.creds = pickle.load(token)
        
        # Si no hay credenciales válidas, autenticar
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.logger.info("Refrescando token de Google Calendar...")
                self.creds.refresh(Request())
            else:
                self.logger.info("Iniciando autenticación OAuth 2.0...")
                self.logger.info("Se abrirá un navegador para autorizar la aplicación")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path,
                    self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            
            # Guardar token para futuros usos
            with open(self.token_path, 'wb') as token:
                pickle.dump(self.creds, token)
            
            self.logger.info("✅ Autenticación exitosa")
        
        # Crear servicio de Calendar
        try:
            self.service = build('calendar', 'v3', credentials=self.creds)
            self.logger.info("✅ Servicio de Google Calendar inicializado")
        except Exception as e:
            self.logger.error(f"❌ Error creando servicio de Calendar: {e}")
    
    def agregar_evento(self, evento: Evento, recordatorio_minutos: int = 60) -> Optional[Dict]:
        """
        Agrega un evento al calendario del usuario.
        
        Args:
            evento: Evento a agregar
            recordatorio_minutos: Minutos antes para recordatorio (default: 60)
            
        Returns:
            Diccionario con información del evento creado o None si falla
        """
        if not self.service:
            self.logger.error("Servicio de Calendar no inicializado")
            return None
        
        try:
            # Construir evento de Calendar
            fecha_inicio = evento.fecha.replace(hour=9, minute=0)  # 9:00 AM por defecto
            fecha_fin = evento.fecha.replace(hour=10, minute=0)    # 1 hora de duración
            
            calendar_event = {
                'summary': evento.titulo,
                'description': f'Evento del calendario académico UNViMe\nCategoría: {evento.categoria}',
                'start': {
                    'dateTime': fecha_inicio.isoformat(),
                    'timeZone': 'America/Argentina/Buenos_Aires',
                },
                'end': {
                    'dateTime': fecha_fin.isoformat(),
                    'timeZone': 'America/Argentina/Buenos_Aires',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': recordatorio_minutos},
                        {'method': 'email', 'minutes': 24 * 60},  # 1 día antes por email
                    ],
                },
                'colorId': self._get_color_por_categoria(evento.categoria),
            }
            
            # Crear evento en el calendario principal
            resultado = self.service.events().insert(
                calendarId='primary',
                body=calendar_event
            ).execute()
            
            self.logger.info(f"✅ Evento agregado: {evento.titulo} ({evento.fecha_legible()})")
            
            return {
                'id': resultado.get('id'),
                'link': resultado.get('htmlLink'),
                'evento': evento.titulo,
                'fecha': evento.fecha_legible()
            }
            
        except HttpError as error:
            self.logger.error(f"❌ Error de Google Calendar API: {error}")
            return None
        except Exception as e:
            self.logger.error(f"❌ Error agregando evento: {e}", exc_info=True)
            return None
    
    def agregar_multiples_eventos(self, eventos: List[Evento]) -> Dict:
        """
        Agrega múltiples eventos al calendario.
        
        Args:
            eventos: Lista de eventos a agregar
            
        Returns:
            Diccionario con estadísticas de la operación
        """
        exitosos = 0
        fallidos = 0
        resultados = []
        
        for evento in eventos:
            resultado = self.agregar_evento(evento)
            if resultado:
                exitosos += 1
                resultados.append(resultado)
            else:
                fallidos += 1
        
        return {
            'total': len(eventos),
            'exitosos': exitosos,
            'fallidos': fallidos,
            'eventos': resultados
        }
    
    def _get_color_por_categoria(self, categoria: str) -> str:
        """
        Retorna el color de Google Calendar según la categoría.
        
        Colors:
        1: Lavender, 2: Sage, 3: Grape, 4: Flamingo,
        5: Banana, 6: Tangerine, 7: Peacock, 8: Graphite,
        9: Blueberry, 10: Basil, 11: Tomato
        """
        colores = {
            'examen': '11',        # Rojo (Tomato)
            'academico': '9',      # Azul (Blueberry)
            'feriado': '10',       # Verde (Basil)
            'receso': '5',         # Amarillo (Banana)
            'institucional': '7',  # Turquesa (Peacock)
            'otro': '8'            # Gris (Graphite)
        }
        return colores.get(categoria.lower(), '9')
    
    def listar_proximos_eventos(self, max_resultados: int = 10) -> List:
        """
        Lista los próximos eventos del calendario (para testing).
        
        Args:
            max_resultados: Número máximo de eventos a retornar
            
        Returns:
            Lista de eventos
        """
        if not self.service:
            return []
        
        try:
            now = datetime.utcnow().isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=max_resultados,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            eventos = events_result.get('items', [])
            
            return eventos
            
        except HttpError as error:
            self.logger.error(f"Error listando eventos: {error}")
            return []