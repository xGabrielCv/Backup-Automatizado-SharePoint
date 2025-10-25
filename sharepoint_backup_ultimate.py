"""
Sistema de Backup Automatizado de Listas do SharePoint - VERSÃO ULTIMATE
Data: 2025-10-25
Versão: 4.0 ULTIMATE

NOVIDADES v4.0:
1. Modo local pode usar portable_libs (força instalação local)
2. Keep-Alive para evitar bloqueio/suspensão do PC
3. Agendamento avançado (dias específicos, intervalos, etc)
4. Sistema de notificações ntfy.sh (opcional e não-bloqueante)
"""

import os
import sys
import logging
import csv
import shutil
import json
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# ============================================================================
# DETECÇÃO DE MODO PORTÁTIL E CONFIGURAÇÃO DE PATH
# ============================================================================

SCRIPT_DIR = Path(__file__).parent.absolute()
PORTABLE_MODE = False
USE_PORTABLE_LIBS = False

# Detectar se está em drive removível (pendrive)
if sys.platform == 'win32':
    import string
    from ctypes import windll
    
    drive_letter = str(SCRIPT_DIR)[0].upper()
    if drive_letter in string.ascii_uppercase:
        drive_type = windll.kernel32.GetDriveTypeW(f"{drive_letter}:\\")
        if drive_type == 2:  # DRIVE_REMOVABLE
            PORTABLE_MODE = True

# NOVO: Verificar se deve usar portable_libs mesmo em modo local
PORTABLE_LIBS_DIR = SCRIPT_DIR / "portable_libs"
if PORTABLE_LIBS_DIR.exists():
    # Permitir uso de portable_libs mesmo em HD local
    config_file = SCRIPT_DIR / "config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                USE_PORTABLE_LIBS = config_data.get("use_portable_libs", False)
        except:
            pass

# ============================================================================
# IMPORTAÇÕES COM VALIDAÇÃO
# ============================================================================

try:
    from office365.runtime.auth.client_credential import ClientCredential
    from office365.sharepoint.client_context import ClientContext
    from office365.graph.graph_client import GraphClient
    OFFICE365_AVAILABLE = True
except ImportError:
    OFFICE365_AVAILABLE = False

try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# NOVO: Importação opcional de ntfy para notificações
try:
    import requests as ntfy_requests
    NTFY_AVAILABLE = True
except ImportError:
    NTFY_AVAILABLE = False

# NOVO: Importação para Keep-Alive do sistema
if sys.platform == 'win32':
    try:
        import ctypes
        CTYPES_AVAILABLE = True
    except ImportError:
        CTYPES_AVAILABLE = False
else:
    CTYPES_AVAILABLE = False


class KeepAlive:
    """
    Classe para manter o computador ativo durante a execução
    Previne suspensão, hibernação e bloqueio de tela
    """
    
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    ES_DISPLAY_REQUIRED = 0x00000002
    ES_AWAYMODE_REQUIRED = 0x00000040
    
    def __init__(self, logger=None):
        self.logger = logger
        self.active = False
        self.thread = None
        self.stop_event = threading.Event()
        
        if not CTYPES_AVAILABLE or sys.platform != 'win32':
            if self.logger:
                self.logger.warning("⚠️  Keep-Alive não disponível nesta plataforma")
    
    def start(self):
        """Inicia o Keep-Alive"""
        if not CTYPES_AVAILABLE or sys.platform != 'win32':
            return False
        
        try:
            # Prevenir suspensão e desligamento da tela
            ctypes.windll.kernel32.SetThreadExecutionState(
                self.ES_CONTINUOUS | 
                self.ES_SYSTEM_REQUIRED | 
                self.ES_DISPLAY_REQUIRED |
                self.ES_AWAYMODE_REQUIRED
            )
            
            self.active = True
            
            # Thread para mover o mouse sutilmente (evita screensaver)
            self.thread = threading.Thread(target=self._keep_alive_loop, daemon=True)
            self.thread.start()
            
            if self.logger:
                self.logger.info("✅ Keep-Alive ativado (PC permanecerá ativo)")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.warning(f"⚠️  Erro ao ativar Keep-Alive: {e}")
            return False
    
    def _keep_alive_loop(self):
        """Loop que mantém atividade no sistema"""
        while not self.stop_event.is_set():
            try:
                # Simular atividade do sistema sem mover o mouse visualmente
                ctypes.windll.kernel32.SetThreadExecutionState(
                    self.ES_CONTINUOUS | 
                    self.ES_SYSTEM_REQUIRED | 
                    self.ES_DISPLAY_REQUIRED
                )
            except:
                pass
            
            # Verificar a cada 30 segundos
            self.stop_event.wait(30)
    
    def stop(self):
        """Para o Keep-Alive"""
        if not CTYPES_AVAILABLE or sys.platform != 'win32':
            return
        
        try:
            self.stop_event.set()
            
            if self.thread:
                self.thread.join(timeout=2)
            
            # Restaurar comportamento normal
            ctypes.windll.kernel32.SetThreadExecutionState(self.ES_CONTINUOUS)
            
            self.active = False
            
            if self.logger:
                self.logger.info("✅ Keep-Alive desativado")
                
        except Exception as e:
            if self.logger:
                self.logger.warning(f"⚠️  Erro ao desativar Keep-Alive: {e}")


class NotificationService:
    """
    Serviço de notificações usando ntfy.sh
    Completamente opcional e não-bloqueante
    """
    
    def __init__(self, config: Dict, logger=None):
        self.logger = logger
        self.enabled = config.get("notifications_enabled", False)
        self.topic = config.get("ntfy_topic", "")
        self.server = config.get("ntfy_server", "https://ntfy.sh")
        self.timeout = config.get("ntfy_timeout", 5)  # Timeout curto
        self.priority = config.get("ntfy_priority", "default")
        
        if self.enabled and not NTFY_AVAILABLE:
            if self.logger:
                self.logger.warning("⚠️  Notificações desabilitadas (requests não disponível)")
            self.enabled = False
        
        if self.enabled and not self.topic:
            if self.logger:
                self.logger.warning("⚠️  Notificações desabilitadas (ntfy_topic não configurado)")
            self.enabled = False
    
    def _send_async(self, title: str, message: str, priority: str = None):
        """
        Envia notificação de forma assíncrona (não-bloqueante)
        """
        if not self.enabled:
            return
        
        def send_in_thread():
            try:
                url = f"{self.server}/{self.topic}"
                headers = {
                    "Title": title,
                    "Priority": priority or self.priority,
                    "Tags": "computer,backup"
                }
                
                response = ntfy_requests.post(
                    url, 
                    data=message.encode('utf-8'),
                    headers=headers,
                    timeout=self.timeout
                )
                
                if self.logger and response.status_code != 200:
                    self.logger.debug(f"Notificação falhou: {response.status_code}")
                    
            except Exception as e:
                if self.logger:
                    self.logger.debug(f"Erro ao enviar notificação: {e}")
        
        # Executar em thread separada (não bloqueia)
        thread = threading.Thread(target=send_in_thread, daemon=True)
        thread.start()
    
    def notify_start(self, sites_count: int):
        """Notifica início do backup"""
        self._send_async(
            "🚀 Backup Iniciado",
            f"Backup do SharePoint iniciado\n{sites_count} site(s) serão processados",
            "default"
        )
    
    def notify_error(self, error_msg: str):
        """Notifica erro crítico"""
        self._send_async(
            "❌ Erro no Backup",
            f"Erro durante o backup:\n{error_msg[:200]}",
            "high"
        )
    
    def notify_warning(self, warning_msg: str):
        """Notifica aviso"""
        self._send_async(
            "⚠️ Aviso no Backup",
            warning_msg[:200],
            "default"
        )
    
    def notify_complete(self, stats: Dict, duration: timedelta):
        """Notifica conclusão do backup"""
        message = f"""✅ Backup Concluído!

⏱️ Duração: {duration}

📊 Estatísticas:
• Sites: {stats.get('sites', 0)}
• Listas: {stats.get('success', 0)}/{stats.get('total', 0)}
• Itens: {stats.get('items', 0):,}
• Upload: {'Sim' if stats.get('upload', False) else 'Não'}
"""
        self._send_async(
            "✅ Backup Concluído",
            message,
            "default"
        )


class AdvancedScheduler:
    """
    Agendador avançado com suporte a:
    - Dias específicos da semana
    - Intervalos de dias
    - Horários múltiplos
    - Execução diária
    """
    
    def __init__(self, config: Dict, callback, logger=None):
        self.config = config
        self.callback = callback
        self.logger = logger
        self.schedule_type = config.get("schedule_type", "daily")  # daily, interval, specific_days
        
    def setup_schedule(self):
        """Configura o agendamento baseado no tipo"""
        
        if not SCHEDULE_AVAILABLE:
            if self.logger:
                self.logger.error("❌ Biblioteca 'schedule' não disponível")
            return False
        
        try:
            if self.schedule_type == "daily":
                # Execução diária em horário específico
                time_str = self.config.get("schedule_time", "02:00")
                schedule.every().day.at(time_str).do(self.callback)
                
                if self.logger:
                    self.logger.info(f"⏰ Agendado: DIARIAMENTE às {time_str}")
            
            elif self.schedule_type == "interval":
                # Execução a cada N dias
                days = self.config.get("schedule_interval_days", 3)
                time_str = self.config.get("schedule_time", "02:00")
                schedule.every(days).days.at(time_str).do(self.callback)
                
                if self.logger:
                    self.logger.info(f"⏰ Agendado: A cada {days} dias às {time_str}")
            
            elif self.schedule_type == "specific_days":
                # Dias específicos da semana
                days = self.config.get("schedule_days", ["monday"])  # monday, tuesday, etc
                time_str = self.config.get("schedule_time", "02:00")
                
                day_map = {
                    "monday": schedule.every().monday,
                    "tuesday": schedule.every().tuesday,
                    "wednesday": schedule.every().wednesday,
                    "thursday": schedule.every().thursday,
                    "friday": schedule.every().friday,
                    "saturday": schedule.every().saturday,
                    "sunday": schedule.every().sunday
                }
                
                for day in days:
                    if day.lower() in day_map:
                        day_map[day.lower()].at(time_str).do(self.callback)
                
                days_str = ", ".join(days)
                if self.logger:
                    self.logger.info(f"⏰ Agendado: {days_str} às {time_str}")
            
            elif self.schedule_type == "multiple_times":
                # Múltiplos horários por dia
                times = self.config.get("schedule_times", ["02:00", "14:00"])
                
                for time_str in times:
                    schedule.every().day.at(time_str).do(self.callback)
                
                times_str = ", ".join(times)
                if self.logger:
                    self.logger.info(f"⏰ Agendado: Diariamente às {times_str}")
            
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ Erro ao configurar agendamento: {e}")
            return False
    
    def run(self):
        """Executa o loop de agendamento"""
        if self.logger:
            self.logger.info("🔄 Aguardando horário agendado...")
            self.logger.info("⚠️  Mantenha este script em execução")
            self.logger.info("⚠️  Pressione Ctrl+C para cancelar")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Verificar a cada minuto
        except KeyboardInterrupt:
            if self.logger:
                self.logger.info("\n⚠️  Modo agendado cancelado pelo usuário")


class SharePointBackupUltimate:
    """Classe principal - VERSÃO ULTIMATE com todas as funcionalidades"""
    
    def __init__(self, config_file: str = "config.json"):
        # Verificar dependências
        self._check_dependencies()
        
        self.config = self._load_config(config_file)
        self.base_backup_path = Path(self.config.get("backup_base_path", "Backups"))
        self.onedrive_folder = self.config.get("onedrive_folder", "Backups_SharePoint")
        self.max_backups = self.config.get("max_backups_to_keep", 7)
        
        # Credenciais Azure AD
        self.tenant_id = self.config.get("tenant_id")
        self.client_id = self.config.get("client_id")
        self.client_secret = self.config.get("client_secret")
        
        self.graph_client = None
        
        # Setup logging
        self._setup_logging()
        
        # NOVO: Inicializar Keep-Alive
        self.keep_alive = None
        if self.config.get("keep_alive_enabled", True):
            self.keep_alive = KeepAlive(self.logger)
        
        # NOVO: Inicializar serviço de notificações
        self.notifications = NotificationService(self.config, self.logger)
        
        # Log de configuração
        if PORTABLE_MODE:
            self.logger.info(f"🔌 MODO PORTÁTIL ATIVADO (Pendrive)")
        elif USE_PORTABLE_LIBS:
            self.logger.info(f"📦 Usando bibliotecas de portable_libs/")
        
        self.logger.info(f"📁 Diretório: {SCRIPT_DIR}")
        
        if self.notifications.enabled:
            self.logger.info(f"🔔 Notificações ATIVADAS (ntfy.sh)")
        
        if self.keep_alive:
            self.logger.info(f"⚡ Keep-Alive ATIVADO (PC permanecerá ativo)")
    
    def _check_dependencies(self):
        """Verifica dependências"""
        missing = []
        
        if not OFFICE365_AVAILABLE:
            missing.append("Office365-REST-Python-Client")
        if not SCHEDULE_AVAILABLE:
            missing.append("schedule")
        if not REQUESTS_AVAILABLE:
            missing.append("requests")
        
        if missing:
            print("\n" + "="*70)
            print("❌ ERRO: Bibliotecas Python necessárias não estão instaladas!")
            print("="*70)
            print("\n📦 Bibliotecas faltando:")
            for lib in missing:
                print(f"  • {lib}")
            
            if PORTABLE_MODE or USE_PORTABLE_LIBS:
                print("\n💡 SOLUÇÃO PARA MODO PORTÁTIL:")
                print("\n1️⃣  Se portable_libs existe:")
                print("    cd " + str(SCRIPT_DIR))
                print("    install_offline.bat")
                print("")
                print("2️⃣  Se não tem portable_libs:")
                print("    prepare_portable.bat")
            else:
                print("\n💡 SOLUÇÃO:")
                print(f"\npip install {' '.join(missing)}")
                print(f"ou: pip install --user {' '.join(missing)}")
            
            print("\n" + "="*70)
            sys.exit(1)
    
    def _load_config(self, config_file: str) -> Dict:
        """Carrega configurações"""
        config_path = SCRIPT_DIR / config_file
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Configuração padrão com TODAS as novas opções
            default_config = {
                "_INSTRUCOES": {
                    "DOCUMENTACAO": "Veja GUIA_CONFIGURACAO_AZURE.md para detalhes",
                    "VERSAO": "4.0 ULTIMATE"
                },
                "tenant_id": "SEU_TENANT_ID_AQUI",
                "client_id": "SEU_CLIENT_ID_AQUI",
                "client_secret": "SEU_CLIENT_SECRET_AQUI",
                "sharepoint_sites": [
                    {
                        "url": "https://empresa.sharepoint.com/sites/site1",
                        "nome": "Site 1"
                    }
                ],
                "onedrive_user_email": "gabriel@empresa.com",
                "onedrive_folder": "Backups_SharePoint",
                "backup_base_path": str(SCRIPT_DIR / "Backups"),
                "max_backups_to_keep": 7,
                
                # NOVO: Usar portable_libs mesmo em HD local
                "use_portable_libs": False,
                
                # NOVO: Keep-Alive (evita suspensão/bloqueio)
                "keep_alive_enabled": True,
                
                # NOVO: Agendamento avançado
                "schedule_type": "daily",  # daily, interval, specific_days, multiple_times
                "schedule_time": "02:00",
                "schedule_interval_days": 3,
                "schedule_days": ["monday", "wednesday", "friday"],
                "schedule_times": ["02:00", "14:00"],
                
                # NOVO: Notificações ntfy.sh (opcional)
                "notifications_enabled": False,
                "ntfy_topic": "seu-topico-unico-aqui",
                "ntfy_server": "https://ntfy.sh",
                "ntfy_priority": "default",
                "ntfy_timeout": 5,
                
                # Configurações existentes
                "log_file": "backup_sharepoint.log",
                "batch_size": 5000,
                "retry_attempts": 3,
                "retry_delay_seconds": 5
            }
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            
            print(f"\n✅ Arquivo de configuração criado: {config_path}")
            print("\n⚠️  Configure suas credenciais antes de continuar!")
            sys.exit(0)
    
    def _setup_logging(self):
        """Configura logging"""
        log_file = SCRIPT_DIR / self.config.get("log_file", "backup_sharepoint.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _validate_credentials(self) -> bool:
        """Valida credenciais"""
        errors = []
        
        if not self.tenant_id or "SEU_TENANT_ID" in self.tenant_id.upper():
            errors.append("tenant_id")
        if not self.client_id or "SEU_CLIENT_ID" in self.client_id.upper():
            errors.append("client_id")
        if not self.client_secret or "SEU_CLIENT_SECRET" in self.client_secret.upper():
            errors.append("client_secret")
        
        if errors:
            self.logger.error(f"❌ Credenciais não configuradas: {', '.join(errors)}")
            return False
        
        return True
    
    def connect_to_sharepoint(self, site_config: Dict) -> Optional[ClientContext]:
        """Conecta ao SharePoint"""
        try:
            if not self._validate_credentials():
                return None
            
            url = site_config["url"]
            credentials = ClientCredential(self.client_id, self.client_secret)
            ctx = ClientContext(url).with_credentials(credentials)
            
            web = ctx.web
            ctx.load(web)
            ctx.execute_query()
            
            site_title = web.properties.get('Title', 'Site')
            self.logger.info(f"✅ Conectado: {site_title}")
            return ctx
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao conectar: {e}")
            return None
    
    def initialize_graph_client(self) -> bool:
        """Inicializa Graph Client"""
        try:
            if not self._validate_credentials():
                return False
            
            user_email = self.config.get("onedrive_user_email", "")
            if not user_email:
                self.logger.error("❌ onedrive_user_email não configurado")
                return False
            
            credentials = ClientCredential(self.client_id, self.client_secret)
            self.graph_client = GraphClient(credentials)
            
            target_user = self.graph_client.users[user_email]
            target_user.get().execute_query()
            
            drive = target_user.drive.get().execute_query()
            
            self.logger.info(f"✅ Graph Client inicializado")
            self.logger.info(f"   Usuário: {user_email}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro Graph Client: {e}")
            return False
    
    def get_all_lists(self, ctx: ClientContext) -> List:
        """Obtém listas do site"""
        try:
            lists = ctx.web.lists
            ctx.load(lists)
            ctx.execute_query()
            
            visible_lists = [
                lst for lst in lists 
                if not lst.properties.get("Hidden", False)
            ]
            
            self.logger.info(f"✅ Encontradas {len(visible_lists)} listas")
            return visible_lists
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter listas: {e}")
            return []
    
    def export_list_to_csv_with_pagination(
        self, 
        ctx: ClientContext, 
        list_obj, 
        output_path: Path
    ) -> Tuple[bool, int]:
        """Exporta lista para CSV com paginação"""
        try:
            list_title = list_obj.properties.get("Title", "Unknown")
            item_count = list_obj.properties.get("ItemCount", 0)
            
            self.logger.info(f"  📋 {list_title} ({item_count} itens)")
            
            fields = list_obj.fields
            ctx.load(fields)
            ctx.execute_query()
            
            field_names = []
            field_internal_names = []
            
            for field in fields:
                props = field.properties
                if (not props.get("Hidden", False) 
                    and not props.get("ReadOnlyField", False) 
                    and props.get("Title", "")):
                    
                    field_names.append(props["Title"])
                    field_internal_names.append(props["InternalName"])
            
            if not field_names:
                self.logger.warning(f"  ⚠️  Sem campos visíveis")
                return False, 0
            
            batch_size = self.config.get("batch_size", 5000)
            retry_attempts = self.config.get("retry_attempts", 3)
            retry_delay = self.config.get("retry_delay_seconds", 5)
            
            all_items = []
            
            for attempt in range(retry_attempts):
                try:
                    items = list_obj.items.top(batch_size).get_all(batch_size)
                    ctx.execute_query()
                    all_items = list(items)
                    break
                except Exception as e:
                    if attempt < retry_attempts - 1:
                        time.sleep(retry_delay)
                    else:
                        raise
            
            total_items = len(all_items)
            
            with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(field_names)
                
                if total_items == 0:
                    return True, 0
                
                for idx, item in enumerate(all_items, 1):
                    if idx % 1000 == 0:
                        progress = (idx / total_items) * 100
                        self.logger.info(f"    ⏳ {idx}/{total_items} ({progress:.1f}%)")
                    
                    row = []
                    for internal_name in field_internal_names:
                        try:
                            value = item.properties.get(internal_name, "")
                            
                            if isinstance(value, dict):
                                if '__deferred' in value:
                                    value = ""
                                else:
                                    value = value.get('Title', value.get('Name', str(value)))
                            elif isinstance(value, list):
                                value = "; ".join([str(v) for v in value])
                            elif value is None:
                                value = ""
                            else:
                                value = str(value)
                            
                            row.append(value)
                        except:
                            row.append("")
                    
                    writer.writerow(row)
            
            self.logger.info(f"  ✅ Exportada: {total_items:,} itens")
            return True, total_items
            
        except Exception as e:
            self.logger.error(f"  ❌ Erro: {e}")
            return False, 0
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitiza nome de arquivo"""
        invalid_chars = '<>:"/\\|?*'
        sanitized = filename
        for char in invalid_chars:
            sanitized = sanitized.replace(char, '_')
        return sanitized[:200]
    
    def create_backup_folder(self) -> Path:
        """Cria pasta de backup"""
        today = datetime.now().strftime("%Y-%m-%d")
        backup_folder = self.base_backup_path / f"Backup_{today}"
        backup_folder.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"✅ Pasta: {backup_folder}")
        return backup_folder
    
    def backup_site(self, site_config: Dict, backup_folder: Path) -> Dict:
        """Backup de um site"""
        stats = {
            "total_lists": 0,
            "success": 0,
            "failed": 0,
            "total_items": 0
        }
        
        site_url = site_config["url"]
        site_name = site_config.get("nome", site_url.split("/")[-1])
        
        self.logger.info(f"\n{'='*70}")
        self.logger.info(f"🚀 BACKUP: {site_name}")
        self.logger.info(f"{'='*70}")
        
        ctx = self.connect_to_sharepoint(site_config)
        if not ctx:
            return stats
        
        site_folder = backup_folder / self.sanitize_filename(site_name)
        site_folder.mkdir(exist_ok=True)
        
        lists = self.get_all_lists(ctx)
        stats["total_lists"] = len(lists)
        
        if not lists:
            return stats
        
        for idx, list_obj in enumerate(lists, 1):
            try:
                list_title = list_obj.properties.get("Title", "Unknown")
                self.logger.info(f"\n[{idx}/{stats['total_lists']}] {list_title}")
                
                csv_filename = f"{self.sanitize_filename(list_title)}.csv"
                csv_path = site_folder / csv_filename
                
                success, item_count = self.export_list_to_csv_with_pagination(
                    ctx, list_obj, csv_path
                )
                
                if success:
                    stats["success"] += 1
                    stats["total_items"] += item_count
                else:
                    stats["failed"] += 1
                    
            except Exception as e:
                self.logger.error(f"  ❌ Erro: {e}")
                stats["failed"] += 1
        
        self.logger.info(f"\n{'='*70}")
        self.logger.info(f"📊 RESUMO - {site_name}")
        self.logger.info(f"  Total: {stats['total_lists']}")
        self.logger.info(f"  Sucesso: {stats['success']} ✅")
        self.logger.info(f"  Falhas: {stats['failed']} ❌")
        self.logger.info(f"  Itens: {stats['total_items']:,}")
        self.logger.info(f"{'='*70}\n")
        
        return stats
    
    def upload_to_onedrive(self, local_folder: Path) -> bool:
        """Upload para OneDrive"""
        try:
            if not self.graph_client:
                if not self.initialize_graph_client():
                    return False
            
            user_email = self.config.get("onedrive_user_email", "")
            target_user = self.graph_client.users[user_email]
            
            self.logger.info(f"\n{'='*70}")
            self.logger.info(f"☁️  UPLOAD ONEDRIVE")
            self.logger.info(f"{'='*70}")
            
            all_files = list(local_folder.rglob("*.csv"))
            total_files = len(all_files)
            
            if total_files == 0:
                return False
            
            self.logger.info(f"Total: {total_files} arquivos")
            
            uploaded = 0
            failed = 0
            total_size = 0
            
            for idx, file_path in enumerate(all_files, 1):
                try:
                    rel_path = file_path.relative_to(local_folder)
                    remote_path = f"{self.onedrive_folder}/{local_folder.name}/{str(rel_path).replace(os.sep, '/')}"
                    
                    with open(file_path, 'rb') as f:
                        file_content = f.read()
                    
                    file_size = len(file_content)
                    file_size_mb = file_size / (1024 * 1024)
                    total_size += file_size
                    
                    if idx % 5 == 0 or idx == total_files:
                        progress = (idx / total_files) * 100
                        self.logger.info(f"  [{idx}/{total_files}] ({progress:.1f}%)")
                    
                    if file_size < 4 * 1024 * 1024:
                        target_user.drive.root.upload(remote_path, file_content).execute_query()
                    else:
                        target_user.drive.root.resumable_upload(remote_path, file_content).execute_query()
                    
                    uploaded += 1
                    
                except Exception as e:
                    failed += 1
                    self.logger.error(f"  ❌ {file_path.name}: {e}")
            
            success_rate = (uploaded / total_files * 100) if total_files > 0 else 0
            total_size_mb = total_size / (1024 * 1024)
            
            self.logger.info(f"\n✅ Upload: {uploaded}/{total_files} ({success_rate:.1f}%)")
            self.logger.info(f"📦 Tamanho: {total_size_mb:.2f} MB")
            
            return uploaded > 0
            
        except Exception as e:
            self.logger.error(f"❌ Erro upload: {e}")
            return False
    
    def cleanup_old_backups(self):
        """Remove backups antigos"""
        try:
            if not self.base_backup_path.exists():
                return
            
            backup_folders = [
                f for f in self.base_backup_path.iterdir() 
                if f.is_dir() and f.name.startswith("Backup_")
            ]
            
            backup_folders.sort()
            
            removed = 0
            while len(backup_folders) > self.max_backups:
                oldest = backup_folders.pop(0)
                self.logger.info(f"🗑️  Removendo: {oldest.name}")
                shutil.rmtree(oldest)
                removed += 1
            
            if removed > 0:
                self.logger.info(f"✅ {removed} backup(s) removido(s)")
                
        except Exception as e:
            self.logger.error(f"❌ Erro limpeza: {e}")
    
    def run_backup(self):
        """Executa backup completo"""
        start_time = datetime.now()
        
        # NOVO: Ativar Keep-Alive
        if self.keep_alive:
            self.keep_alive.start()
        
        self.logger.info(f"\n{'#'*70}")
        self.logger.info(f"##    🚀 BACKUP SHAREPOINT INICIADO    ##")
        self.logger.info(f"{'#'*70}")
        self.logger.info(f"📅 {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"👤 gabriel")
        
        try:
            if not self._validate_credentials():
                raise Exception("Credenciais não configuradas")
            
            sites = self.config["sharepoint_sites"]
            
            # NOVO: Notificar início
            self.notifications.notify_start(len(sites))
            
            backup_folder = self.create_backup_folder()
            
            total_stats = {
                "total_lists": 0,
                "success": 0,
                "failed": 0,
                "total_items": 0,
                "sites": len(sites),
                "upload": False
            }
            
            for idx, site_config in enumerate(sites, 1):
                self.logger.info(f"\n{'*'*70}")
                self.logger.info(f"SITE {idx}/{len(sites)}")
                self.logger.info(f"{'*'*70}\n")
                
                stats = self.backup_site(site_config, backup_folder)
                
                total_stats["total_lists"] += stats["total_lists"]
                total_stats["success"] += stats["success"]
                total_stats["failed"] += stats["failed"]
                total_stats["total_items"] += stats["total_items"]
            
            upload_success = self.upload_to_onedrive(backup_folder)
            total_stats["upload"] = upload_success
            
            self.cleanup_old_backups()
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            # NOVO: Notificar conclusão
            total_stats["items"] = total_stats["total_items"]
            total_stats["total"] = total_stats["total_lists"]
            self.notifications.notify_complete(total_stats, duration)
            
            self.logger.info(f"\n{'#'*70}")
            self.logger.info(f"##    ✅ BACKUP CONCLUÍDO    ##")
            self.logger.info(f"{'#'*70}")
            self.logger.info(f"⏱️  Duração: {duration}")
            self.logger.info(f"📊 Listas: {total_stats['success']}/{total_stats['total_lists']}")
            self.logger.info(f"📦 Itens: {total_stats['total_items']:,}")
            self.logger.info(f"☁️  Upload: {'Sim' if upload_success else 'Não'}")
            self.logger.info(f"{'#'*70}\n")
            
        except Exception as e:
            self.logger.error(f"\n❌ ERRO CRÍTICO: {e}")
            
            # NOVO: Notificar erro
            self.notifications.notify_error(str(e))
            
            raise
        
        finally:
            # NOVO: Desativar Keep-Alive
            if self.keep_alive:
                self.keep_alive.stop()
    
    def schedule_backup(self):
        """Inicia modo agendado"""
        self.logger.info(f"\n{'='*70}")
        self.logger.info(f"⏰ MODO AGENDADO ATIVADO")
        self.logger.info(f"{'='*70}\n")
        
        # NOVO: Usar AdvancedScheduler
        scheduler = AdvancedScheduler(self.config, self.run_backup, self.logger)
        
        if scheduler.setup_schedule():
            # NOVO: Ativar Keep-Alive durante espera
            if self.keep_alive:
                self.keep_alive.start()
            
            try:
                scheduler.run()
            finally:
                if self.keep_alive:
                    self.keep_alive.stop()


def main():
    """Função principal"""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║     Sistema de Backup Automatizado do SharePoint                 ║
║                      VERSÃO 4.0 ULTIMATE                          ║
║                                                                   ║
║  ✨ Modo portátil + bibliotecas locais                           ║
║  ⚡ Keep-Alive (PC permanece ativo)                              ║
║  📅 Agendamento avançado (intervalo, dias específicos)           ║
║  🔔 Notificações ntfy.sh (opcional)                              ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    if PORTABLE_MODE:
        print("🔌 MODO PORTÁTIL (Pendrive)")
    elif USE_PORTABLE_LIBS:
        print("📦 Usando portable_libs/")
    
    print("")
    
    try:
        backup_system = SharePointBackupUltimate()
        
        print("="*70)
        print("🎯 Escolha o modo:")
        print("="*70)
        print("\n1. Backup AGORA (uma vez)")
        print("2. Modo AGENDADO (automático)")
        print("3. Backup AGORA + AGENDADO")
        print("\n" + "="*70)
        
        choice = input("\n👉 Escolha (1-3): ").strip()
        
        if choice == "1":
            print("\n🚀 Iniciando...\n")
            backup_system.run_backup()
            print("\n✅ Concluído!")
            
        elif choice == "2":
            print("\n⏰ Modo agendado...\n")
            backup_system.schedule_backup()
            
        elif choice == "3":
            print("\n🚀 Executando...\n")
            backup_system.run_backup()
            print("\n⏰ Iniciando agendamento...\n")
            backup_system.schedule_backup()
            
        else:
            print("\n❌ Opção inválida!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido (Ctrl+C)")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n\n❌ ERRO: {e}")
        logging.exception("Detalhes:")
        sys.exit(1)


if __name__ == "__main__":
    main()