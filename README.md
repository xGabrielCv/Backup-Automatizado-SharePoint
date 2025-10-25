# 🚀 Sistema de Backup Automatizado do SharePoint 
 
**Data:** 2025-10-25  
**Versão:** 4.0 ULTIMATE  
**Status:** ✅ Pronto para produção

---

## 🌟 Novidades da Versão 4.0 ULTIMATE

### ✨ Novos Recursos

1. **🔌 Modo Portátil Aprimorado**
   - Agora funciona em HD local também usando `portable_libs/`
   - Configure `"use_portable_libs": true` no `config.json`

2. **⚡ Keep-Alive Inteligente**
   - PC permanece ativo durante execução
   - Previne suspensão, hibernação e bloqueio de tela
   - Thread não-bloqueante em segundo plano

3. **📅 Agendamento Avançado**
   - **Diário:** Executa todo dia em horário específico
   - **Intervalo:** A cada X dias (ex: a cada 3 dias)
   - **Dias específicos:** Segunda, quarta e sexta (exemplo)
   - **Múltiplos horários:** Várias vezes por dia

4. **🔔 Notificações Push (Opcional)**
   - Integração com ntfy.sh
   - Notificações de início, erros e conclusão
   - Não-bloqueante (executa em thread separada)
   - Timeout curto para não atrasar o backup

---

## 📦 Estrutura do Projeto v4.0

```
SharePoint_Backup/
├── 📄 sharepoint_backup_ultimate.py    ← Script principal v4.0
├── ⚙️  config.json                      ← Configurações (com novos parâmetros)
├── 🔧 prepare_portable.bat             ← Preparar modo portátil
├── 💾 install_offline.bat              ← Instalador offline
├── ▶️  executar_backup.bat             ← Atalho de execução
├── 🔍 verificar_instalacao.bat         ← Verificar ambiente
├── 🔔 testar_notificacoes.bat          ← Testar ntfy.sh
├── 📚 GUIA_CONFIGURACAO_AZURE.md       ← Guia Azure AD
├── 📖 README_PORTABLE.md               ← Guia modo portátil
├── 📖 README_NOTIFICACOES.md           ← Guia notificações
├── 📖 README_AGENDAMENTO.md            ← Guia agendamento avançado
├── 📝 CHANGELOG_v4.0.md                ← Novidades v4.0
├── 📂 portable_libs/                   ← Bibliotecas Python (.whl)
│   ├── Office365_REST_Python_Client-*.whl
│   ├── schedule-*.whl
│   └── requests-*.whl
└── 📂 Backups/                         ← Backups gerados
    ├── Backup_2025-10-25/
    │   ├── Site1/
    │   │   ├── Lista1.csv
    │   │   └── Lista2.csv
    │   └── Site2/
    │       └── ListaA.csv
    └── backup_sharepoint.log
```

---

## 🚀 Início Rápido

### Pré-requisitos

- ✅ Python 3.7 ou superior
- ✅ Acesso aos sites SharePoint
- ✅ Azure App Registration configurado
- ✅ (Opcional) Celular com app ntfy.sh

### Instalação Rápida

**Opção 1: Com Internet**
```bash
pip install Office365-REST-Python-Client schedule requests
python sharepoint_backup_ultimate.py
```

**Opção 2: Sem Internet (Modo Portátil)**
```bash
# Em um PC com internet:
prepare_portable.bat

# No PC sem internet:
install_offline.bat
executar_backup.bat
```

---

## ⚙️ Configuração Detalhada

### 1. Credenciais Azure AD (Obrigatório)

```json
{
    "tenant_id": "12345678-1234-1234-1234-123456789abc",
    "client_id": "87654321-4321-4321-4321-cba987654321",
    "client_secret": "AbC123XyZ~..."
}
```

### 2. Sites SharePoint (Obrigatório)

```json
{
    "sharepoint_sites": [
        {
            "url": "https://empresa.sharepoint.com/sites/vendas",
            "nome": "Site Vendas"
        },
        {
            "url": "https://empresa.sharepoint.com/sites/rh",
            "nome": "Site RH"
        }
    ]
}
```

### 3. OneDrive (Obrigatório)

```json
{
    "onedrive_user_email": "gabrielcarvalho54@empresa.com",
    "onedrive_folder": "Backups_SharePoint"
}
```

### 4. NOVO: Modo Portátil Local (Opcional)

```json
{
    "use_portable_libs": true
}
```

**Quando usar:**
- Você está em um PC com HD local (não pendrive)
- Mas quer usar as bibliotecas de `portable_libs/`
- Útil para ambientes sem acesso ao pip

### 5. NOVO: Keep-Alive (Recomendado)

```json
{
    "keep_alive_enabled": true
}
```

**O que faz:**
- Mantém o PC ativo durante o backup
- Previne suspensão automática
- Previne hibernação
- Previne bloqueio de tela
- Não afeta o desempenho

### 6. NOVO: Agendamento Avançado

#### Opção A: Diário (Padrão)
```json
{
    "schedule_type": "daily",
    "schedule_time": "02:00"
}
```

#### Opção B: Intervalo de Dias
```json
{
    "schedule_type": "interval",
    "schedule_interval_days": 3,
    "schedule_time": "02:00"
}
```
*Executa a cada 3 dias às 02:00*

#### Opção C: Dias Específicos da Semana
```json
{
    "schedule_type": "specific_days",
    "schedule_days": ["monday", "wednesday", "friday"],
    "schedule_time": "02:00"
}
```
*Executa segunda, quarta e sexta às 02:00*

#### Opção D: Múltiplos Horários
```json
{
    "schedule_type": "multiple_times",
    "schedule_times": ["02:00", "14:00", "20:00"]
}
```
*Executa 3 vezes por dia*

### 7. NOVO: Notificações Push (Opcional)

```json
{
    "notifications_enabled": true,
    "ntfy_topic": "backup-sharepoint-gabrielcarvalho54",
    "ntfy_server": "https://ntfy.sh",
    "ntfy_priority": "default",
    "ntfy_timeout": 5
}
```

**Como configurar:**

1. Instale o app ntfy no celular:
   - Android: Play Store → "ntfy"
   - iOS: App Store → "ntfy"
   - Web: https://ntfy.sh/app

2. Crie um tópico ÚNICO (ex: `backup-sharepoint-seu-nome-123`)

3. No app, adicione esse tópico

4. Configure no `config.json`

5. Teste: `testar_notificacoes.bat`

**Notificações enviadas:**
- 🚀 Início do backup
- ⚠️ Avisos importantes
- ❌ Erros críticos
- ✅ Conclusão com estatísticas

---

## 🎯 Modos de Execução

### 1️⃣ Backup Imediato

```bash
python sharepoint_backup_ultimate.py
# Escolha opção 1
```

### 2️⃣ Modo Agendado

```bash
python sharepoint_backup_ultimate.py
# Escolha opção 2
# Deixe o terminal aberto
```

### 3️⃣ Backup + Agendado

```bash
python sharepoint_backup_ultimate.py
# Escolha opção 3
```

---

## 📊 Exemplo de Log Completo

```
2025-10-25 02:00:00 - INFO - ######################################################################
2025-10-25 02:00:00 - INFO - ##    🚀 BACKUP SHAREPOINT INICIADO    ##
2025-10-25 02:00:00 - INFO - ######################################################################
2025-10-25 02:00:00 - INFO - 📅 2025-10-25 02:00:00
2025-10-25 02:00:00 - INFO - 👤 gabrielcarvalho54
2025-10-25 02:00:00 - INFO - ⚡ Keep-Alive ATIVADO (PC permanecerá ativo)
2025-10-25 02:00:00 - INFO - 🔔 Notificações ATIVADAS (ntfy.sh)
2025-10-25 02:00:01 - INFO - ✅ Pasta: Backups/Backup_2025-10-25
2025-10-25 02:00:02 - INFO - ======================================================================
2025-10-25 02:00:02 - INFO - 🚀 BACKUP: Site Vendas
2025-10-25 02:00:02 - INFO - ======================================================================
2025-10-25 02:00:03 - INFO - ✅ Conectado: Site Vendas
2025-10-25 02:00:04 - INFO - ✅ Encontradas 15 listas
2025-10-25 02:00:05 - INFO - 
2025-10-25 02:00:05 - INFO - [1/15] Clientes
2025-10-25 02:00:05 - INFO -   📋 Clientes (1234 itens)
2025-10-25 02:00:12 - INFO -   ✅ Exportada: 1,234 itens
...
2025-10-25 02:15:45 - INFO - ======================================================================
2025-10-25 02:15:45 - INFO - ☁️  UPLOAD ONEDRIVE
2025-10-25 02:15:45 - INFO - ======================================================================
2025-10-25 02:15:46 - INFO - ✅ Graph Client inicializado
2025-10-25 02:15:46 - INFO -    Usuário: gabrielcarvalho54@empresa.com
2025-10-25 02:15:47 - INFO - Total: 15 arquivos
2025-10-25 02:18:23 - INFO - 
2025-10-25 02:18:23 - INFO - ✅ Upload: 15/15 (100.0%)
2025-10-25 02:18:23 - INFO - 📦 Tamanho: 45.67 MB
2025-10-25 02:18:24 - INFO - 🗑️  Removendo: Backup_2025-10-18
2025-10-25 02:18:25 - INFO - ✅ 1 backup(s) removido(s)
2025-10-25 02:18:25 - INFO - 
2025-10-25 02:18:25 - INFO - ######################################################################
2025-10-25 02:18:25 - INFO - ##    ✅ BACKUP CONCLUÍDO    ##
2025-10-25 02:18:25 - INFO - ######################################################################
2025-10-25 02:18:25 - INFO - ⏱️  Duração: 0:18:25
2025-10-25 02:18:25 - INFO - 📊 Listas: 15/15
2025-10-25 02:18:25 - INFO - 📦 Itens: 12,345
2025-10-25 02:18:25 - INFO - ☁️  Upload: Sim
2025-10-25 02:18:25 - INFO - ######################################################################
2025-10-25 02:18:26 - INFO - ✅ Keep-Alive desativado
```

---

## 🔧 Troubleshooting

### Problema: PC suspende durante backup

**Solução:**
```json
{
    "keep_alive_enabled": true
}
```

### Problema: Notificações não chegam

**Verificar:**
1. App ntfy instalado no celular?
2. Tópico adicionado no app?
3. Tópico no config.json está correto?
4. Execute: `testar_notificacoes.bat`

### Problema: Backup não executa no horário agendado

**Verificar:**
1. Terminal/prompt ainda está aberto?
2. PC está ligado no horário agendado?
3. Keep-Alive está ativado?

### Problema: Bibliotecas não encontradas (modo portátil)

**Solução:**
```bash
cd portable_libs
install_offline.bat
```

---

## 📚 Documentação Adicional

- 📖 [GUIA_CONFIGURACAO_AZURE.md](GUIA_CONFIGURACAO_AZURE.md) - Configurar Azure AD
- 📖 [README_PORTABLE.md](README_PORTABLE.md) - Modo portátil detalhado
- 📖 [README_NOTIFICACOES.md](README_NOTIFICACOES.md) - Configurar notificações
- 📖 [README_AGENDAMENTO.md](README_AGENDAMENTO.md) - Agendamento avançado
- 📖 [CHANGELOG_v4.0.md](CHANGELOG_v4.0.md) - Novidades desta versão

---

## 🎓 Perguntas Frequentes

### 1. O Keep-Alive funciona em Linux/Mac?

Atualmente apenas Windows. Em Linux/Mac, use `caffeinate` ou `systemd-inhibit`.

### 2. As notificações são obrigatórias?

Não! São totalmente opcionais. Configure `"notifications_enabled": false`.

### 3. Posso usar meu próprio servidor ntfy?

Sim! Configure `"ntfy_server": "https://meu-servidor.com"`.

### 4. O que acontece se a notificação falhar?

Nada! O backup continua normalmente. Notificações são não-bloqueantes.

### 5. Posso agendar para fim de semana?

Sim! Use:
```json
{
    "schedule_type": "specific_days",
    "schedule_days": ["saturday", "sunday"]
}
```

---

### Logs

Verifique: `backup_sharepoint.log`

### Testar Componentes

```bash
verificar_instalacao.bat    # Verifica ambiente
testar_notificacoes.bat     # Testa ntfy.sh
```


**Última atualização:** 2025-10-25 18:01:41 UTC
