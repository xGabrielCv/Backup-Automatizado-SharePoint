# 🔔 Guia Completo de Notificações - SharePoint Backup v4.0

**Versão:** 4.0 ULTIMATE  
**Autor:** gabrielcarvalho54  
**Data:** 2025-10-25  
**Atualizado:** 2025-10-25 18:04:07 UTC

---

## 📱 Introdução

O sistema de notificações do SharePoint Backup v4.0 usa **ntfy.sh**, um serviço gratuito e open-source de notificações push que funciona em:

- 📱 **Android** (via app)
- 📱 **iOS** (via app)
- 💻 **Desktop** (via navegador)
- 🌐 **Web** (via PWA)

### ✨ Características

- ✅ **Completamente opcional** - não afeta o funcionamento do backup
- ✅ **Não-bloqueante** - executa em thread separada
- ✅ **Timeout curto** (5 segundos) - não atrasa o backup
- ✅ **Gratuito e sem cadastro** - só precisa de um tópico único
- ✅ **Privado** - ninguém mais recebe suas notificações

---

## 🚀 Configuração Rápida (5 minutos)

### Passo 1: Instalar o App ntfy

**Android:**
1. Abra a Play Store
2. Busque por "ntfy"
3. Instale o app oficial (ícone de sino preto)

**iOS:**
1. Abra a App Store
2. Busque por "ntfy"
3. Instale o app oficial

**Desktop/Web:**
- Acesse: https://ntfy.sh/app

### Passo 2: Criar um Tópico Único

⚠️ **IMPORTANTE:** Use um nome ÚNICO e difícil de adivinhar!

**Exemplos de tópicos RUINS (não use):**
- ❌ `backup`
- ❌ `sharepoint`
- ❌ `teste`

**Exemplos de tópicos BONS:**
- ✅ `backup-sharepoint-gabrielcarvalho54-2025`
- ✅ `sp-backup-empresa-abc-secret-987`
- ✅ `meu-backup-unico-xyz123`

**Dica:** Use seu nome + empresa + número aleatório

### Passo 3: Adicionar Tópico no App

1. Abra o app ntfy
2. Toque no **+** (adicionar)
3. Digite seu tópico único
4. Toque em "Subscribe"

### Passo 4: Configurar no config.json

Edite o arquivo `config.json`:

```json
{
    "notifications_enabled": true,
    "ntfy_topic": "backup-sharepoint-gabrielcarvalho54-2025",
    "ntfy_server": "https://ntfy.sh",
    "ntfy_priority": "default",
    "ntfy_timeout": 5
}
```

### Passo 5: Testar

Execute o script de teste:

```batch
testar_notificacoes.bat
```

Ou manualmente:

```bash
curl -d "Teste de notificação!" https://ntfy.sh/seu-topico-aqui
```

Você deve receber a notificação no celular/desktop em segundos!

---

## ⚙️ Configurações Avançadas

### Parâmetros do config.json

```json
{
    "notifications_enabled": true,
    "ntfy_topic": "seu-topico-unico",
    "ntfy_server": "https://ntfy.sh",
    "ntfy_priority": "default",
    "ntfy_timeout": 5
}
```

#### `notifications_enabled` (boolean)

Ativa ou desativa as notificações.

**Valores:**
- `true` - Notificações ativadas
- `false` - Notificações desativadas (padrão)

**Exemplo:**
```json
"notifications_enabled": true
```

#### `ntfy_topic` (string)

O tópico único que você criou.

**Regras:**
- Apenas letras, números, hífens e underscores
- Mínimo 3 caracteres
- Máximo 64 caracteres
- Case-sensitive (diferencia maiúsculas/minúsculas)

**Exemplo:**
```json
"ntfy_topic": "backup-sharepoint-gabrielcarvalho54-2025"
```

#### `ntfy_server` (string)

URL do servidor ntfy.

**Valores:**
- `https://ntfy.sh` - Servidor público oficial (padrão)
- `https://seu-servidor.com` - Seu servidor privado

**Exemplo:**
```json
"ntfy_server": "https://ntfy.sh"
```

#### `ntfy_priority` (string)

Prioridade das notificações.

**Valores:**
- `min` - Prioridade mínima (sem som)
- `low` - Prioridade baixa
- `default` - Prioridade padrão (recomendado)
- `high` - Prioridade alta (com som)
- `urgent` - Urgente (som persistente)

**Exemplo:**
```json
"ntfy_priority": "default"
```

**Quando usar cada prioridade:**
- `default` - Backups normais (recomendado)
- `high` - Erros críticos
- `urgent` - Falhas que precisam atenção imediata

#### `ntfy_timeout` (integer)

Tempo máximo (em segundos) para enviar a notificação.

**Valores:**
- Mínimo: `1`
- Recomendado: `5`
- Máximo: `30`

**Exemplo:**
```json
"ntfy_timeout": 5
```

⚠️ **Importante:** Um timeout baixo garante que o backup não seja atrasado se o servidor ntfy estiver lento.

---

## 📬 Tipos de Notificações

### 1. 🚀 Início do Backup

**Quando:** Ao iniciar o processo de backup

**Exemplo:**
```
🚀 Backup Iniciado

Backup do SharePoint iniciado
2 site(s) serão processados
```

**Prioridade:** `default`

---

### 2. ⚠️ Avisos

**Quando:** Algo não crítico acontece

**Exemplos:**
- Lista sem permissão de acesso
- Lista vazia
- Keep-Alive não disponível

**Exemplo:**
```
⚠️ Aviso no Backup

Lista 'Documentos Confidenciais' sem permissão de acesso.
Pulando para a próxima lista.
```

**Prioridade:** `default`

---

### 3. ❌ Erros Críticos

**Quando:** Erro que impede o backup

**Exemplos:**
- Falha na autenticação
- Credenciais inválidas
- Site inacessível
- Falha no upload OneDrive

**Exemplo:**
```
❌ Erro no Backup

Erro durante o backup:
AADSTS7000215: Invalid client secret is provided.
```

**Prioridade:** `high`

---

### 4. ✅ Conclusão com Sucesso

**Quando:** Backup finalizado com sucesso

**Exemplo:**
```
✅ Backup Concluído!

⏱️ Duração: 0:18:25

📊 Estatísticas:
• Sites: 2
• Listas: 15/15
• Itens: 12,345
• Upload: Sim
```

**Prioridade:** `default`

---

## 🛠️ Troubleshooting

### Problema 1: Não recebo notificações

#### Checklist:

**1. App instalado?**
```bash
# Verifique se o app está instalado no celular
```

**2. Tópico adicionado no app?**
```bash
# Abra o app → Verifique se seu tópico está na lista
```

**3. Tópico correto no config.json?**
```json
"ntfy_topic": "backup-sharepoint-gabrielcarvalho54-2025"
```

**4. Notificações habilitadas?**
```json
"notifications_enabled": true
```

**5. Testar manualmente:**
```bash
testar_notificacoes.bat
```

Ou:
```bash
curl -d "Teste manual" https://ntfy.sh/seu-topico
```

**6. Verifique permissões do app:**
- Android: Configurações → Apps → ntfy → Notificações → Permitir
- iOS: Configurações → Notificações → ntfy → Permitir

---

### Problema 2: Notificações atrasam o backup

**Causa:** Timeout muito alto ou servidor ntfy lento

**Solução:**
```json
{
    "ntfy_timeout": 3
}
```

Reduza o timeout para 3 segundos (ou menos).

---

### Problema 3: Muitas notificações

**Causa:** Modo `high` ou `urgent` envia notificações muito agressivas

**Solução:**
```json
{
    "ntfy_priority": "default"
}
```

Use prioridade `default` ou `low`.

---

### Problema 4: Erro "requests not available"

**Causa:** Biblioteca `requests` não instalada

**Solução:**
```bash
pip install requests
```

Ou se estiver em modo portátil:
```bash
install_offline.bat
```

---

### Problema 5: Outras pessoas recebem minhas notificações

**Causa:** Tópico muito genérico

**Solução:** Use um tópico ÚNICO e complexo:
```json
"ntfy_topic": "backup-sharepoint-gabrielcarvalho54-empresa-abc-2025-xyz987"
```

---

## 🔒 Segurança e Privacidade

### Como o ntfy.sh funciona?

1. Você escolhe um **tópico** (ex: `backup-sp-gabriel-2025`)
2. O script envia mensagens para esse tópico
3. Qualquer pessoa que **souber** o tópico pode receber as mensagens
4. **Não há autenticação** - a segurança vem da complexidade do tópico

### ⚠️ O que NÃO fazer:

❌ **Usar tópicos genéricos:**
- `backup`, `sharepoint`, `teste`, etc.

❌ **Compartilhar seu tópico publicamente:**
- Não poste em fóruns, redes sociais, etc.

❌ **Incluir informações sensíveis nas mensagens:**
- O script já evita isso, mas fique atento

### ✅ Boas Práticas:

✅ **Use tópicos únicos e longos:**
```
backup-sharepoint-gabrielcarvalho54-empresa-xyz-2025-secret123
```

✅ **Não compartilhe seu tópico:**
- Mantenha privado como uma senha

✅ **Rotacione o tópico periodicamente:**
- Mude a cada 6 meses para maior segurança

✅ **Use servidor privado (opcional):**
- Monte seu próprio servidor ntfy para controle total

---

## 🏠 Servidor Privado (Avançado)

Se você quer **controle total** e **mais privacidade**, pode hospedar seu próprio servidor ntfy.

### Opção 1: Docker (Recomendado)

```bash
docker run -p 80:80 -d binwiederhier/ntfy serve
```

### Opção 2: Instalação Manual

```bash
# Linux
curl -sSL https://ntfy.sh/install.sh | bash
sudo systemctl start ntfy
```

### Configurar no config.json

```json
{
    "ntfy_server": "https://meu-servidor.empresa.com",
    "ntfy_topic": "backup-sharepoint"
}
```

**Vantagens:**
- ✅ Controle total
- ✅ Privacidade garantida
- ✅ Sem limites de taxa

**Desvantagens:**
- ❌ Requer servidor próprio
- ❌ Manutenção necessária

---

## 📊 Exemplos de Uso

### Exemplo 1: Notificações Básicas

```json
{
    "notifications_enabled": true,
    "ntfy_topic": "backup-sp-gabriel-2025",
    "ntfy_server": "https://ntfy.sh",
    "ntfy_priority": "default",
    "ntfy_timeout": 5
}
```

**Resultado:**
- Notificações em prioridade normal
- Timeout de 5 segundos
- Usa servidor público ntfy.sh

---

### Exemplo 2: Apenas Erros Críticos

Para receber **apenas** notificações de erro, edite o código:

```python
# Em sharepoint_backup_ultimate.py, comente as linhas:
# self.notifications.notify_start(len(sites))
# self.notifications.notify_complete(total_stats, duration)

# Mantenha apenas:
# self.notifications.notify_error(str(e))
```

---

### Exemplo 3: Servidor Privado

```json
{
    "notifications_enabled": true,
    "ntfy_topic": "backup-sharepoint",
    "ntfy_server": "https://ntfy.minhaempresa.com",
    "ntfy_priority": "high",
    "ntfy_timeout": 10
}
```

---

## 🧪 Testar Notificações

### Método 1: Script Automático

```bash
testar_notificacoes.bat
```

Digite seu tópico e verifique se recebe a notificação.

---

### Método 2: curl (Manual)

**Windows (PowerShell):**
```powershell
Invoke-WebRequest -Method POST -Body "Teste de notificação!" -Uri "https://ntfy.sh/seu-topico"
```

**Windows (curl):**
```bash
curl -d "Teste de notificação!" https://ntfy.sh/seu-topico
```

**Linux/Mac:**
```bash
curl -d "Teste de notificação!" https://ntfy.sh/seu-topico
```

---

### Método 3: Python

```python
import requests

requests.post(
    "https://ntfy.sh/seu-topico",
    data="Teste de notificação!".encode('utf-8'),
    headers={
        "Title": "Teste",
        "Priority": "default",
        "Tags": "test"
    }
)
```

---

## 📱 App ntfy - Dicas e Truques

### 1. Prioridade de Notificações

No app, você pode configurar prioridades diferentes para cada tópico:

1. Toque no tópico
2. Configurações (⚙️)
3. "Minimum priority"
4. Escolha: `default`, `high`, `urgent`

---

### 2. Som Customizado

**Android:**
1. Toque no tópico
2. Configurações → Som de notificação
3. Escolha um som

**iOS:**
1. Configurações do iOS → Notificações → ntfy
2. Sons → Escolha um som

---

### 3. Desativar Temporariamente

**Pausar por X horas:**
1. Toque no tópico
2. Configurações → Pausar notificações
3. Escolha duração (1h, 4h, 8h, etc.)

---

### 4. Histórico de Notificações

O app mantém histórico de todas as notificações:

1. Abra o tópico
2. Role para cima para ver notificações antigas

---

### 5. Múltiplos Dispositivos

Você pode receber no celular E no desktop:

1. Instale o app em todos os dispositivos
2. Adicione o mesmo tópico em todos

Todos receberão as notificações simultaneamente!

---

## 🎨 Customização Avançada

### Adicionar Emojis

O código já usa emojis nas notificações:
- 🚀 Início
- ⚠️ Avisos
- ❌ Erros
- ✅ Sucesso

### Adicionar Links

Edite o código para incluir links:

```python
def notify_complete(self, stats: Dict, duration: timedelta):
    message = f"""✅ Backup Concluído!
    
⏱️ Duração: {duration}

📊 Ver detalhes: https://onedrive.com/seu-backup
"""
    self._send_async("✅ Backup Concluído", message, "default")
```

---

## 🔍 Logs de Notificações

As notificações são registradas no log principal:

```
2025-10-25 02:00:00 - INFO - 🔔 Notificações ATIVADAS (ntfy.sh)
2025-10-25 02:00:01 - DEBUG - Notificação enviada: Backup Iniciado
2025-10-25 02:18:25 - DEBUG - Notificação enviada: Backup Concluído
```

Se houver erro ao enviar:
```
2025-10-25 02:00:01 - DEBUG - Erro ao enviar notificação: Timeout
```

⚠️ **Importante:** Erros de notificação NÃO param o backup!

---

## ❓ Perguntas Frequentes

### 1. As notificações são gratuitas?

**Sim!** O ntfy.sh é completamente gratuito e open-source.

---

### 2. Preciso criar conta?

**Não!** Basta escolher um tópico e começar a usar.

---

### 3. Há limite de notificações?

No servidor público (ntfy.sh):
- **12.500 mensagens por IP por dia**
- Suficiente para centenas de backups

No servidor privado:
- **Sem limites!**

---

### 4. As notificações são seguras?

- ✅ Mensagens enviadas via **HTTPS**
- ✅ Servidor não armazena mensagens por muito tempo
- ⚠️ Qualquer pessoa com o tópico pode receber

**Dica:** Use tópico único e complexo!

---

### 5. Funciona offline?

- ❌ Precisa de internet para enviar
- ✅ Mas se falhar, o backup continua normalmente

---

### 6. Posso usar no iPhone?

**Sim!** O app ntfy está disponível para iOS na App Store.

---

### 7. E se eu esquecer meu tópico?

Está salvo no `config.json`:

```json
"ntfy_topic": "seu-topico-aqui"
```

---

## 📚 Recursos Adicionais

### Links Úteis

- 🌐 Site oficial: https://ntfy.sh
- 📖 Documentação: https://docs.ntfy.sh
- 💻 GitHub: https://github.com/binwiederhier/ntfy
- 💬 Discord: https://discord.gg/cT7ECsZj9w

### Alternativas ao ntfy.sh

Se preferir outras soluções:

1. **Pushover** (pago)
   - https://pushover.net
   - $5 vitalício

2. **Telegram Bot** (gratuito)
   - Requer criação de bot
   - Mais complexo

3. **Email** (gratuito)
   - Requer configuração SMTP
   - Mais lento

---

## 🎯 Resumo Rápido

### Para Começar:

1. ✅ Instale app ntfy no celular
2. ✅ Crie tópico único: `backup-sharepoint-seu-nome-123`
3. ✅ Adicione tópico no app
4. ✅ Configure no `config.json`:
   ```json
   {
       "notifications_enabled": true,
       "ntfy_topic": "backup-sharepoint-seu-nome-123"
   }
   ```
5. ✅ Teste: `testar_notificacoes.bat`

### Pronto! 🎉

Agora você receberá notificações de:
- 🚀 Início do backup
- ⚠️ Avisos importantes
- ❌ Erros críticos
- ✅ Conclusão com estatísticas

---

**Última atualização:** 2025-10-25 18:04:07 UTC  
**Versão:** 4.0 ULTIMATE  
**Autor:** gabrielcarvalho54