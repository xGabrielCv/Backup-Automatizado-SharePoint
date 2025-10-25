# 🔌 Guia de Uso - Modo Portátil (Pendrive)

## 📋 Situação

Você precisa executar o backup em um computador da empresa que:
- ✅ Tem Python instalado
- ❌ Bloqueia instalação de bibliotecas via `pip install` (internet)
- ❌ Não tem as bibliotecas necessárias instaladas

## 💡 Solução: Modo Portátil

Execute tudo direto do pendrive com bibliotecas pré-baixadas!

---

## 🚀 Preparação (Em casa ou computador com internet)

### Passo 1: Download das Bibliotecas

Execute no computador com internet:

```batch
prepare_portable.bat
```

Isso irá:
1. Criar pasta `portable_libs` com todas as bibliotecas
2. Baixar Office365-REST-Python-Client, schedule, requests
3. Criar scripts auxiliares

### Passo 2: Configurar Credenciais

Edite o arquivo `config.json` com suas credenciais do Azure:

```json
{
    "tenant_id": "seu-tenant-id-aqui",
    "client_id": "seu-client-id-aqui",
    "client_secret": "seu-client-secret-aqui",
    "sharepoint_sites": [...],
    "onedrive_user_email": "gabrielcarvalho54@empresa.com"
}
```

### Passo 3: Copiar para Pendrive

Copie TODA a pasta para o pendrive:

```
E:\SharePoint_Backup\
├── sharepoint_backup_portable.py
├── config.json
├── portable_libs\
│   ├── Office365_REST_Python_Client-*.whl
│   ├── schedule-*.whl
│   ├── requests-*.whl
│   └── ... (outras dependências)
├── install_offline.bat
├── executar_backup.bat
└── README_PORTABLE.md
```

---

## 💻 Execução (No computador da empresa)

### Cenário A: Python + Internet (raro)

Se o PC tem Python E internet:

```batch
python sharepoint_backup_portable.py
```

### Cenário B: Python SEM Internet (comum)

#### 1. Instalar Bibliotecas Offline

```batch
install_offline.bat
```

Isso instala as bibliotecas do pendrive para o Python local.

#### 2. Executar Backup

```batch
executar_backup.bat
```

Ou manualmente:

```batch
python sharepoint_backup_portable.py
```

### Cenário C: Sem Permissão para Instalar

Se não pode instalar bibliotecas nem offline, configure o Python para usar diretamente do pendrive:

```batch
set PYTHONPATH=E:\SharePoint_Backup\portable_libs
python sharepoint_backup_portable.py
```

---

## 🔧 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'office365'"

**Causa:** Bibliotecas não instaladas.

**Solução:**
```batch
cd E:\SharePoint_Backup
install_offline.bat
```

### Erro: "pip install blocked by company policy"

**Solução:** Use instalação offline:
```batch
pip install --no-index --find-links=portable_libs Office365-REST-Python-Client schedule requests
```

### Erro: "Access Denied" ao instalar

**Solução:** Instale para o usuário:
```batch
pip install --user --no-index --find-links=portable_libs Office365-REST-Python-Client
```

### Script não detecta pendrive

**Verificar:** O script detecta automaticamente drives removíveis no Windows. Se falhar:
```python
# No código, força modo portátil:
PORTABLE_MODE = True
```

---

## 📊 Estrutura de Pastas Criadas

Após execução, no pendrive terá:

```
E:\SharePoint_Backup\
├── Backups\
│   ├── Backup_2025-10-25\
│   │   ├── Site1\
│   │   │   ├── Lista1.csv
│   │   │   └── Lista2.csv
│   │   └── Site2\
│   │       └── ListaA.csv
│   └── Backup_2025-10-24\
├── backup_sharepoint.log
└── ... (arquivos do script)
```

---

## 🔒 Segurança no Pendrive

⚠️ **ATENÇÃO**: O pendrive contém credenciais sensíveis!

### Recomendações:

1. **Criptografe o pendrive:**
   - Windows: BitLocker
   - Alternativa: VeraCrypt

2. **Proteja o config.json:**
   ```batch
   attrib +h config.json
   ```

3. **Use pendrive com senha:**
   - Pendrives com autenticação biométrica
   - Ou software de criptografia

4. **Não deixe desacompanhado:**
   - Sempre leve o pendrive com você
   - Não empreste para terceiros

---

## ⚡ Dicas de Performance

### Para backups grandes:

1. **Use pendrive USB 3.0+:**
   - Velocidade de escrita: mínimo 50 MB/s

2. **Comprima backups antigos:**
   ```python
   # Adicione ao config.json:
   "compress_old_backups": true
   ```

3. **Agende para horário de baixo uso:**
   ```json
   "schedule_time": "02:00"
   ```

---

## 📞 Checklist de Execução

### Antes de sair de casa:
- [ ] Bibliotecas baixadas (`portable_libs/` populado)
- [ ] `config.json` configurado com credenciais
- [ ] Testou uma vez em casa
- [ ] Pendrive criptografado
- [ ] Backup do `config.json` em local seguro

### No computador da empresa:
- [ ] Conectou pendrive
- [ ] Executou `install_offline.bat` (se necessário)
- [ ] Executou `executar_backup.bat`
- [ ] Aguardou conclusão
- [ ] Verificou logs para erros
- [ ] Confirmou upload no OneDrive

### Antes de remover pendrive:
- [ ] Backup concluído (verificar log)
- [ ] Arquivos CSV gerados
- [ ] Upload OneDrive bem-sucedido
- [ ] Nenhum processo Python rodando
- [ ] "Ejetar" pendrive com segurança

---

## 🎓 Comandos Úteis

### Verificar versão Python:
```batch
python --version
```

### Listar bibliotecas instaladas:
```batch
pip list
```

### Espaço disponível no pendrive:
```batch
dir E:\ 
```

### Limpar backups antigos manualmente:
```batch
rmdir /s /q "E:\SharePoint_Backup\Backups\Backup_2025-10-20"
```

---

## 📈 Monitoramento

### Verificar se está rodando:
```batch
tasklist | findstr python
```

### Ver log em tempo real:
```batch
type backup_sharepoint.log
```

### Última execução:
Verifique a data da pasta mais recente em `Backups/`

---

**Última atualização:** 2025-10-25  
**Versão:** 2.1 PORTABLE  
**Autor:** gabrielcarvalho54