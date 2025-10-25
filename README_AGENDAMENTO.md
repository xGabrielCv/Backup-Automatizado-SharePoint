# 📅 Guia Completo de Agendamento Avançado - SharePoint Backup v4.0

**Versão:** 4.0 ULTIMATE  
**Autor:** gabrielcarvalho54  
**Data:** 2025-10-25  
**Atualizado:** 2025-10-25 18:04:07 UTC

---

## 🎯 Introdução

O SharePoint Backup v4.0 oferece **4 modos de agendamento** flexíveis para atender diferentes necessidades:

1. **📆 Diário** - Todo dia no mesmo horário
2. **🔄 Intervalo** - A cada X dias
3. **📍 Dias Específicos** - Dias da semana escolhidos
4. **⏰ Múltiplos Horários** - Várias vezes por dia

---

## 🚀 Configuração Rápida

### Modo 1: Diário (Padrão)

Executa **todo dia** em um horário específico.

**Configuração:**
```json
{
    "schedule_type": "daily",
    "schedule_time": "02:00"
}
```

**Quando usar:**
- ✅ Backups diários regulares
- ✅ Horário de baixo uso (madrugada)
- ✅ Política de backup diária da empresa

**Exemplo:**
```json
{
    "schedule_type": "daily",
    "schedule_time": "03:30"
}
```
*Executa todo dia às 03:30*

---

### Modo 2: Intervalo de Dias

Executa **a cada X dias** em um horário específico.

**Configuração:**
```json
{
    "schedule_type": "interval",
    "schedule_interval_days": 3,
    "schedule_time": "02:00"
}
```

**Quando usar:**
- ✅ Backups menos frequentes (dados mudam pouco)
- ✅ Economizar recursos
- ✅ Sites com pouca atividade

**Exemplos:**

**A cada 3 dias:**
```json
{
    "schedule_type": "interval",
    "schedule_interval_days": 3,
    "schedule_time": "02:00"
}
```

**A cada semana (7 dias):**
```json
{
    "schedule_type": "interval",
    "schedule_interval_days": 7,
    "schedule_time": "23:00"
}
```

**A cada 15 dias:**
```json
{
    "schedule_type": "interval",
    "schedule_interval_days": 15,
    "schedule_time": "00:30"
}
```

---

### Modo 3: Dias Específicos da Semana

Executa **apenas nos dias da semana** que você escolher.

**Configuração:**
```json
{
    "schedule_type": "specific_days",
    "schedule_days": ["monday", "wednesday", "friday"],
    "schedule_time": "02:00"
}
```

**Dias disponíveis:**
- `monday` - Segunda-feira
- `tuesday` - Terça-feira
- `wednesday` - Quarta-feira
- `thursday` - Quinta-feira
- `friday` - Sexta-feira
- `saturday` - Sábado
- `sunday` - Domingo

**Quando usar:**
- ✅ Backups apenas em dias úteis
- ✅ Evitar fins de semana
- ✅ Padrão específico da empresa

**Exemplos:**

**Apenas dias úteis:**
```json
{
    "schedule_type": "specific_days",
    "schedule_days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
    "schedule_time": "02:00"
}
```

**Apenas início e meio da semana:**
```json
{
    "schedule_type": "specific_days",
    "schedule_days": ["monday", "wednesday"],
    "schedule_time": "03:00"
}
```

**Apenas fins de semana:**
```json
{
    "schedule_type": "specific_days",
    "schedule_days": ["saturday", "sunday"],
    "schedule_time": "10:00"
}
```

**Apenas segunda-feira:**
```json
{
    "schedule_type": "specific_days",
    "schedule_days": ["monday"],
    "schedule_time": "01:00"
}
```

---

### Modo 4: Múltiplos Horários

Executa **várias vezes por dia** nos horários especificados.

**Configuração:**
```json
{
    "schedule_type": "multiple_times",
    "schedule_times": ["02:00", "14:00", "20:00"]
}
```

**Quando usar:**
- ✅ Backups incrementais frequentes
- ✅ Dados mudam muito durante o dia
- ✅ Redundância extra

**Exemplos:**

**2 vezes por dia (manhã e noite):**
```json
{
    "schedule_type": "multiple_times",
    "schedule_times": ["03:00", "20:00"]
}
```

**3 vezes por dia (início, meio, fim do expediente):**
```json
{
    "schedule_type": "multiple_times",
    "schedule_times": ["08:00", "13:00", "18:00"]
}
```

**A cada 6 horas:**
```json
{
    "schedule_type": "multiple_times",
    "schedule_times": ["00:00", "06:00", "12:00", "18:00"]
}
```

---

## ⏰ Formato de Horário

### Formato Aceito

Use o formato **24 horas** com dois dígitos:

✅ **Correto:**
- `"02:00"` - 2 da manhã
- `"14:30"` - 2:30 da tarde
- `"23:59"` - 11:59 da noite
- `"00:00"` - Meia-noite

❌ **Errado:**
- `"2:00"` - Falta o zero à esquerda
- `"14:5"` - Falta o zero nos minutos
- `"2pm"` - Não use AM/PM
- `"25:00"` - Hora inválida

### Dicas de Horário

**Horários recomendados para backup:**
- `01:00` - `04:00` - Madrugada (baixo uso)
- `12:00` - `13:00` - Horário de almoço
- `22:00` - `23:59` - Final da noite

**Evite:**
- `08:00` - `09:00` - Início do expediente (alto uso)
- `17:00` - `18:00` - Final do expediente (alto uso)

---

## 📊 Exemplos Práticos

### Cenário 1: Empresa Pequena

**Necessidade:**
- Backup diário
- Horário de madrugada
- Sem necessidade de backup nos finais de semana

**Solução:**
```json
{
    "schedule_type": "specific_days",
    "schedule_days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
    "schedule_time": "02:00"
}
```

---

### Cenário 2: Empresa com Dados Críticos

**Necessidade:**
- Backups frequentes
- 3 vezes por dia
- Todos os dias da semana

**Solução:**
```json
{
    "schedule_type": "multiple_times",
    "schedule_times": ["03:00", "12:00", "21:00"]
}
```

---

### Cenário 3: Site com Pouca Atividade

**Necessidade:**
- Backup semanal suficiente
- Economia de recursos
- Apenas dias úteis

**Solução:**
```json
{
    "schedule_type": "specific_days",
    "schedule_days": ["monday"],
    "schedule_time": "03:00"
}
```

---

### Cenário 4: Conformidade Legal

**Necessidade:**
- Backup quinzenal obrigatório
- Horário específico

**Solução:**
```json
{
    "schedule_type": "interval",
    "schedule_interval_days": 15,
    "schedule_time": "00:00"
}
```

---

### Cenário 5: Equipe Internacional

**Necessidade:**
- Backups em horários que não afetem nenhum fuso
- 2 backups diários

**Solução:**
```json
{
    "schedule_type": "multiple_times",
    "schedule_times": ["02:00", "14:00"]
}
```

---

## 🔧 Como Funciona Tecnicamente

### Biblioteca schedule

O sistema usa a biblioteca Python `schedule`:

```python
import schedule

# Diário
schedule.every().day.at("02:00").do(backup)

# Intervalo
schedule.every(3).days.at("02:00").do(backup)

# Dias específicos
schedule.every().monday.at("02:00").do(backup)
schedule.every().wednesday.at("02:00").do(backup)

# Múltiplos horários
schedule.every().day.at("02:00").do(backup)
schedule.every().day.at("14:00").do(backup)
```

### Loop de Verificação

O script verifica a cada **60 segundos** se é hora de executar:

```python
while True:
    schedule.run_pending()
    time.sleep(60)  # Verifica a cada minuto
```

⚠️ **Importante:** O script precisa estar **rodando** para o agendamento funcionar!

---

## 🖥️ Executar em Background

### Windows - Task Scheduler

Para que o backup execute mesmo com você deslogado:

#### Método 1: GUI (Interface Gráfica)

1. Abra "Task Scheduler" (Agendador de Tarefas)
2. Clique em "Create Basic Task"
3. Nome: "SharePoint Backup v4.0"
4. Trigger: "When the computer starts"
5. Action: "Start a program"
6. Program: `python`
7. Arguments: `"C:\caminho\sharepoint_backup_ultimate.py"`
8. Working directory: `C:\caminho\`
9. ✅ "Run whether user is logged on or not"
10. ✅ "Run with highest privileges"

#### Método 2: Linha de Comando

```batch
schtasks /create /tn "SharePoint Backup" /tr "python C:\caminho\sharepoint_backup_ultimate.py" /sc onstart /ru SYSTEM
```

---

### Linux - systemd

#### 1. Criar arquivo de serviço

```bash
sudo nano /etc/systemd/system/sharepoint-backup.service
```

Conteúdo:
```ini
[Unit]
Description=SharePoint Backup Service
After=network.target

[Service]
Type=simple
User=seu-usuario
WorkingDirectory=/caminho/do/script
ExecStart=/usr/bin/python3 /caminho/sharepoint_backup_ultimate.py
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 2. Habilitar e iniciar

```bash
sudo systemctl daemon-reload
sudo systemctl enable sharepoint-backup
sudo systemctl start sharepoint-backup
```

#### 3. Verificar status

```bash
sudo systemctl status sharepoint-backup
```

---

### Linux - cron (Alternativa)

⚠️ **Atenção:** cron não mantém o script rodando continuamente!

Use apenas para execuções pontuais:

```bash
crontab -e
```

Adicione:
```bash
# Diariamente às 02:00
0 2 * * * /usr/bin/python3 /caminho/sharepoint_backup_ultimate.py
```

---

## 🛠️ Troubleshooting

### Problema 1: Backup não executa no horário

#### Causa 1: Script não está rodando

**Verificar:**
- Terminal/prompt está aberto?
- Script está em execução?

**Solução:**
Execute o script em modo agendado:
```bash
python sharepoint_backup_ultimate.py
# Escolha opção 2 ou 3
```

#### Causa 2: PC desligado no horário

**Verificar:**
- PC estava ligado no horário agendado?
- Keep-Alive está ativado?

**Solução:**
1. Deixe o PC ligado 24/7, OU
2. Use Task Scheduler para iniciar com o PC

#### Causa 3: PC suspendeu

**Verificar:**
```json
"keep_alive_enabled": true
```

**Solução:**
Ative o Keep-Alive no `config.json`.

---

### Problema 2: Horário errado

#### Causa: Fuso horário

O script usa o **horário local** do sistema.

**Verificar horário do sistema:**

Windows:
```batch
time
```

Linux:
```bash
date
```

**Ajustar:**
- Windows: Painel de Controle → Data e Hora
- Linux: `sudo timedatectl set-timezone America/Sao_Paulo`

---

### Problema 3: Script trava

#### Causa: Erro durante o backup

**Verificar log:**
```
backup_sharepoint.log
```

**Solução:**
O script deve continuar mesmo com erros. Verifique:
1. Credenciais corretas?
2. Sites acessíveis?
3. Espaço em disco suficiente?

---

### Problema 4: Backup executou 2 vezes

#### Causa 1: Dois scripts rodando

**Verificar:**

Windows:
```batch
tasklist | findstr python
```

Linux:
```bash
ps aux | grep python
```

**Solução:**
Mate processos duplicados.

#### Causa 2: Configuração duplicada

**Verificar:**
- Task Scheduler tem tarefa duplicada?
- crontab tem entrada duplicada?

**Solução:**
Remova duplicatas.

---

## 📊 Logs de Agendamento

O sistema registra quando está em modo agendado:

```
2025-10-25 18:00:00 - INFO - ======================================================================
2025-10-25 18:00:00 - INFO - ⏰ MODO AGENDADO ATIVADO
2025-10-25 18:00:00 - INFO - ======================================================================
2025-10-25 18:00:00 - INFO - ⏰ Agendado: DIARIAMENTE às 02:00
2025-10-25 18:00:00 - INFO - 🔄 Aguardando horário agendado...
2025-10-25 18:00:00 - INFO - ⚠️  Mantenha este script em execução
```

Quando chega a hora:
```
2025-10-26 02:00:00 - INFO - ######################################################################
2025-10-26 02:00:00 - INFO - ##    🚀 BACKUP SHAREPOINT INICIADO    ##
2025-10-26 02:00:00 - INFO - ######################################################################
```

---

## 💡 Dicas e Best Practices

### 1. Escolher o Modo Certo

| Frequência | Modo Recomendado |
|------------|------------------|
| Todo dia | `daily` |
| 2-3x por semana | `specific_days` |
| 1x por semana | `interval` (7 dias) |
| Várias vezes/dia | `multiple_times` |

### 2. Horários Ideais

**Para backups rápidos (<30min):**
- Madrugada: `02:00` - `04:00`

**Para backups longos (>1h):**
- Noite: `22:00` - `01:00`
- Fim de semana: Sábado/Domingo

### 3. Keep-Alive

**Sempre ative:**
```json
"keep_alive_enabled": true
```

Especialmente se:
- PC tem suspensão automática
- Screensaver ativo
- Política de energia agressiva

### 4. Testar Primeiro

Antes de agendar, **teste manualmente**:
```bash
python sharepoint_backup_ultimate.py
# Opção 1 - Executar agora
```

Verifique:
- ✅ Backup funciona?
- ✅ Upload OneDrive funciona?
- ✅ Logs estão corretos?

### 5. Monitoramento

Configure **notificações** para saber quando executar:
```json
{
    "notifications_enabled": true,
    "ntfy_topic": "backup-sharepoint-gabriel-2025"
}
```

### 6. Redundância

Para dados críticos, considere:
- Múltiplos horários por dia
- Backup local + OneDrive + servidor
- Agendamento em múltiplas máquinas

---

## ❓ Perguntas Frequentes

### 1. Posso combinar modos?

**Não diretamente**, mas você pode executar múltiplos scripts:

```
Script 1: Diário às 02:00
Script 2: Sábado às 10:00
```

### 2. O que acontece se perder o horário?

O backup **NÃO** executa retroativamente. Ele aguarda o próximo horário agendado.

### 3. Posso mudar o agendamento sem reiniciar?

**Não**. Após mudar o `config.json`, reinicie o script.

### 4. Quanto tempo antes devo ligar o PC?

O script verifica a cada **60 segundos**. Ligue pelo menos **5 minutos antes**.

### 5. Funciona em múltiplos fusos horários?

**Sim**, mas usa o horário **local do sistema**.

### 6. Posso agendar para segundos específicos?

**Não**. Apenas horário (HH:MM). Segundos não são suportados.

---

## 🎨 Configurações Avançadas

### Combinar com Notificações

```json
{
    "schedule_type": "daily",
    "schedule_time": "02:00",
    "notifications_enabled": true,
    "ntfy_topic": "backup-sp-gabriel",
    "keep_alive_enabled": true
}
```

**Resultado:**
- ⏰ Backup agendado às 02:00
- 🔔 Notificação quando executar
- ⚡ PC fica ativo durante execução

---

### Backup em Horário de Pico (Não Recomendado)

Se **realmente precisar** durante o expediente:

```json
{
    "schedule_type": "daily",
    "schedule_time": "10:00",
    "batch_size": 1000,
    "retry_delay_seconds": 10
}
```

Reduza `batch_size` para diminuir carga.

---

## 📚 Recursos Adicionais

### Documentação da Biblioteca schedule

- 📖 Docs: https://schedule.readthedocs.io/
- 💻 GitHub: https://github.com/dbader/schedule

### Alternativas

Para agendamento mais complexo, considere:

1. **APScheduler** - Agendamento avançado Python
2. **Celery** - Tarefas assíncronas
3. **Airflow** - Orquestração de workflows

---

## 🎯 Resumo Rápido

### Configuração Básica:

```json
{
    "schedule_type": "daily",
    "schedule_time": "02:00",
    "keep_alive_enabled": true
}
```

### Executar:

```bash
python sharepoint_backup_ultimate.py
# Opção 2 ou 3
```

### Verificar Logs:

```
backup_sharepoint.log
```

### Pronto! 🎉

---

**Última atualização:** 2025-10-25 18:04:07 UTC  
**Versão:** 4.0 ULTIMATE  
**Autor:** gabrielcarvalho54