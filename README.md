# 🚀 Sistema de Backup Automatizado do SharePoint

<p align="center">
  <img src="https://img.shields.io/badge/version-4.0%20ULTIMATE-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.7%2B-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg" alt="Platform">

  <img src="https://img.shields.io/github/stars/xGabrielCv/Backup-Automatizado-SharePoint?style=social" alt="Stars">
</p>

<p align="center">
  <strong>Sistema completo e automatizado para backup de listas do SharePoint com upload para OneDrive</strong>
</p>

<p align="center">
  <a href="#-recursos">Recursos</a> •
  <a href="#-início-rápido">Início Rápido</a> •
  <a href="#-documentação">Documentação</a> •
</p>

---

## ✨ Recursos Principais

- ✅ **Autenticação Segura** - Via Azure App Registration (suporta MFA)
- ✅ **Backup Múltiplos Sites** - Processa vários sites SharePoint simultaneamente
- ✅ **Exportação CSV** - Todas as listas em formato UTF-8 (compatível Excel)
- ✅ **Paginação Automática** - Suporta listas com +5.000 itens
- ✅ **Upload OneDrive** - Sincronização automática via Microsoft Graph API
- ✅ **Modo Portátil** - Execução direto de pendrive (ambientes restritos)
- ✅ **Keep-Alive** - Mantém PC ativo durante backup longo
- ✅ **Agendamento Avançado** - 4 modos (diário, intervalo, dias específicos, múltiplos horários)
- ✅ **Notificações Push** - Via ntfy.sh (opcional e não-bloqueante)
- ✅ **Logs Detalhados** - Monitoramento completo de todas operações
- ✅ **Limpeza Automática** - Remove backups antigos automaticamente

## 🎯 Casos de Uso

- 📊 Conformidade e auditoria (manter histórico de listas)
- 🔄 Migração de dados entre ambientes
- 🛡️ Backup preventivo antes de mudanças críticas
- 📈 Análise de dados offline (exportar para Excel/Power BI)
- 🏢 Ambientes corporativos com políticas rígidas de segurança

## 🚀 Início Rápido

### Pré-requisitos

```bash
# Python 3.7 ou superior
python --version

# Pip atualizado
pip --version
```

### Instalação

**Opção 1: Com Internet**
```bash
# Clone o repositório
git clone https://github.com/xGabrielCv/Backup-Automatizado-SharePoint.git
cd Backup-Automatizado-SharePoint

# Configure suas credenciais
# Edite config.json com suas credenciais do Azure AD

# Execute
python sharepoint_backup_ultimate.py
```

**Opção 2: Modo Portátil (Sem Internet)**
```bash
# Em um PC com internet, prepare o ambiente
prepare_portable.bat

# Copie a pasta para o pendrive
# No PC sem internet
install_offline.bat
executar_backup.bat
```

### Configuração Mínima

```json
{
    "tenant_id": "seu-tenant-id",
    "client_id": "seu-client-id",
    "client_secret": "seu-secret",
    "sharepoint_sites": [
        {
            "url": "https://empresa.sharepoint.com/sites/site1",
            "nome": "Site Principal"
        }
    ],
    "onedrive_user_email": "usuario@empresa.com"
}
```

## 📖 Documentação

- 📘 [Guia Completo de Configuração](docs/GUIA_CONFIGURACAO_AZURE.md)
- 📗 [Modo Portátil (Pendrive)](docs/README_PORTABLE.md)
- 📙 [Notificações Push](docs/README_NOTIFICACOES.md)
- 📕 [Agendamento Avançado](docs/README_AGENDAMENTO.md)
- 📝 [Changelog v4.0](docs/CHANGELOG_v4.0.md)

## 🎬 Demo

### Execução Normal
```
╔═══════════════════════════════════════════════════════════════════╗
║     Sistema de Backup Automatizado do SharePoint v4.0            ║
╚═══════════════════════════════════════════════════════════════════╝

🎯 Escolha o modo:
1. Backup AGORA (uma vez)
2. Modo AGENDADO (automático)
3. Backup AGORA + AGENDADO

👉 Escolha (1-3): 1

🚀 Iniciando backup...
✅ Conectado: Site Vendas
✅ Encontradas 15 listas
📋 Exportando: Clientes (1,234 itens)
✅ Lista exportada: 1,234 itens
...
☁️  Upload para OneDrive
✅ Upload: 15/15 arquivos (100%)
✅ BACKUP CONCLUÍDO!
```


### Dashboard de Execução
```
######################################################################
##    🚀 BACKUP SHAREPOINT INICIADO    ##
######################################################################
📅 Data/Hora: 2025-01-25 02:00:00
💻 Sistema: PORTÁTIL (Pendrive)
⚡ Keep-Alive ATIVADO
🔔 Notificações ATIVADAS
```

### Notificação Push
```
🔔 Notificação no Celular:
┌──────────────────────────┐
│ ✅ Backup Concluído!     │
│                          │
│ ⏱️ Duração: 0:18:25      │
│                          │
│ 📊 Estatísticas:         │
│ • Listas: 15/15          │
│ • Itens: 12,345          │
│ • Upload: Sim            │
└──────────────────────────┘
```

## 🏗️ Estrutura do Projeto

```
Backup-Automatizado-SharePoint/
├── 📄 sharepoint_backup_ultimate.py    # Script principal
├── ⚙️ config.json                      # Configurações
├── 📋 requirements.txt                 # Dependências Python
├── 🔧 prepare_portable.bat             # Preparar modo portátil
├── 💾 install_offline.bat              # Instalador offline
├── ▶️ executar_backup.bat              # Atalho execução
├── 🔍 verificar_instalacao.bat         # Verificar ambiente
├── 🔔 testar_notificacoes.bat          # Testar ntfy.sh
├── 📂 docs/                            # Documentação
│   ├── GUIA_CONFIGURACAO_AZURE.md
│   ├── README_PORTABLE.md
│   ├── README_NOTIFICACOES.md
│   ├── README_AGENDAMENTO.md
│   └── CHANGELOG_v4.0.md
├── 📂 portable_libs/                   # Bibliotecas offline
└── 📂 Backups/                         # Backups gerados
```

## 🛠️ Tecnologias

- **Python 3.7+** - Linguagem principal
- **Office365-REST-Python-Client** - Integração SharePoint/OneDrive
- **Microsoft Graph API** - Upload OneDrive
- **schedule** - Agendamento de tarefas
- **ntfy.sh** - Notificações push
- **Azure AD** - Autenticação segura

## 🔧 Configuração do Azure AD

1. Acesse [Azure Portal](https://portal.azure.com)
2. Azure Active Directory → App registrations → New registration
3. Configure permissões:
   - `Sites.Read.All` (Application)
   - `Files.ReadWrite.All` (Application)
   - `User.Read.All` (Application)
4. Grant admin consent
5. Copie: Tenant ID, Client ID, Client Secret

📖 [Guia detalhado](docs/GUIA_CONFIGURACAO_AZURE.md)

## 📅 Modos de Agendamento

### Diário
```json
{
    "schedule_type": "daily",
    "schedule_time": "02:00"
}
```

### Intervalo (a cada X dias)
```json
{
    "schedule_type": "interval",
    "schedule_interval_days": 3,
    "schedule_time": "02:00"
}
```

### Dias Específicos
```json
{
    "schedule_type": "specific_days",
    "schedule_days": ["monday", "wednesday", "friday"],
    "schedule_time": "02:00"
}
```

### Múltiplos Horários
```json
{
    "schedule_type": "multiple_times",
    "schedule_times": ["02:00", "14:00", "20:00"]
}
```

## 🔔 Notificações

Configure notificações push opcionais:

1. Instale app [ntfy](https://ntfy.sh) no celular
2. Crie tópico único: `backup-sharepoint-seu-nome-123`
3. Configure:
```json
{
    "notifications_enabled": true,
    "ntfy_topic": "backup-sharepoint-seu-nome-123"
}
```
4. Teste: `testar_notificacoes.bat`

## 🐛 Troubleshooting



### Erro: Credenciais inválidas
- Verifique tenant_id, client_id, client_secret
- Confirme que o admin consent foi dado
- Aguarde 5-10 minutos após criar o app

### PC suspende durante backup
```json
{
    "keep_alive_enabled": true
}
```

### Mais problemas?
Consulte a [documentação completa](docs/README_FULL.md) ou abra uma [issue](https://github.com/xGabrielCv/Backup-Automatizado-SharePoint/issues).

## 📊 Estatísticas

- ⭐ **0 Issues abertas** (por enquanto!)
- 🔀 **0 Pull Requests** (contribuições bem-vindas!)
- 📥 **Downloads:** Em breve
- 👥 **Contribuidores:** 1

## 🤝 Contribuindo

Contribuições são bem-vindas! 

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add: nova funcionalidade'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Ideias para Contribuir

- 🐧 Suporte completo para Linux/Mac
- 🔐 Criptografia de backups
- 📧 Notificações via email
- 🗜️ Compressão de arquivos
- 🌐 Interface web para configuração
- 🐳 Dockerfile para containerização
- 📊 Dashboard de estatísticas

## 👤 Autor

**xGabrielCv**

- GitHub: [@xGabrielCv](https://github.com/xGabrielCv)
- Projeto: [Backup-Automatizado-SharePoint](https://github.com/xGabrielCv/Backup-Automatizado-SharePoint)

## 📞 Suporte

- 📖 [Documentação](docs/README_FULL.md)
- 🐛 [Reportar Bug](https://github.com/xGabrielCv/Backup-Automatizado-SharePoint/issues)
- 💡 [Solicitar Feature](https://github.com/xGabrielCv/Backup-Automatizado-SharePoint/issues)
- ⭐ [Dar Star no Projeto](https://github.com/xGabrielCv/Backup-Automatizado-SharePoint)

---

<p align="center">
  Desenvolvido com ❤️ por <a href="https://github.com/xGabrielCv">xGabrielCv</a>
</p>

<p align="center">
  Se este projeto te ajudou, considere dar uma ⭐!
</p>