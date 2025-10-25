# 📘 Guia Completo de Configuração do Azure App Registration

## 🎯 Visão Geral

Este sistema usa **autenticação baseada em aplicação (App-Only)** através do Azure Active Directory, que:
- ✅ Suporta Multi-Factor Authentication (MFA/2FA)
- ✅ Não requer interação do usuário
- ✅ É ideal para automação e scripts agendados
- ✅ Mais seguro que senha em texto puro

---

## 📋 Pré-requisitos

- Acesso ao Azure Portal (https://portal.azure.com)
- Permissões de **Administrador Global** ou **Administrador de Aplicações**
- Acesso aos sites SharePoint que serão backupeados

---

## 🚀 Passo a Passo

### 1️⃣ Acessar Azure Portal

1. Acesse: https://portal.azure.com
2. Faça login com sua conta corporativa

### 2️⃣ Criar App Registration

1. No menu lateral, procure por **"Azure Active Directory"**
2. No menu da esquerda, clique em **"App registrations"**
3. Clique em **"+ New registration"**

### 3️⃣ Configurar o Aplicativo

**Nome:**
```
SharePoint Backup App
```

**Supported account types:**
- Selecione: **"Accounts in this organizational directory only (Single tenant)"**

**Redirect URI:**
- Deixe em branco (não é necessário)

Clique em **"Register"**

### 4️⃣ Copiar IDs Importantes

Após criar, você verá a página "Overview". **COPIE** e **SALVE**:

1. **Application (client) ID**
   - Exemplo: `12345678-1234-1234-1234-123456789abc`
   - Este é o seu `client_id`

2. **Directory (tenant) ID**
   - Exemplo: `87654321-4321-4321-4321-cba987654321`
   - Este é o seu `tenant_id`

### 5️⃣ Criar Client Secret

1. No menu lateral do app, clique em **"Certificates & secrets"**
2. Clique na aba **"Client secrets"**
3. Clique em **"+ New client secret"**

**Configuração:**
- Description: `SharePoint Backup Secret`
- Expires: Selecione **"24 months"** (ou conforme política da empresa)

4. Clique em **"Add"**
5. ⚠️ **IMPORTANTE**: Copie o **"Value"** IMEDIATAMENTE (ele só aparece uma vez!)
   - Exemplo: `AbC123XyZ789~AbC123XyZ789.AbC123XyZ789`
   - Este é o seu `client_secret`

### 6️⃣ Configurar Permissões de API

1. No menu lateral, clique em **"API permissions"**
2. Clique em **"+ Add a permission"**

#### Adicionar permissões do Microsoft Graph:

1. Clique em **"Microsoft Graph"**
2. Clique em **"Application permissions"** (NÃO Delegated)
3. Procure e marque:
   - `Files.ReadWrite.All` (para upload no OneDrive)
   - `User.Read.All` (para identificar usuários)
4. Clique em **"Add permissions"**

#### Adicionar permissões do SharePoint:

1. Clique novamente em **"+ Add a permission"**
2. Clique em **"SharePoint"**
3. Clique em **"Application permissions"**
4. Procure e marque:
   - `Sites.Read.All` (para ler listas)
5. Clique em **"Add permissions"**

### 7️⃣ Conceder Consentimento do Administrador

⚠️ **CRÍTICO**: Este passo requer permissões de administrador!

1. Na página "API permissions", clique em **"✅ Grant admin consent for [sua empresa]"**
2. Clique em **"Yes"** para confirmar
3. Aguarde até que todas as permissões mostrem **"Granted for [sua empresa]"** com um ✅ verde

---

## 📝 Atualizar config.json

Agora edite o arquivo `config.json` com os valores copiados:

```json
{
    "tenant_id": "87654321-4321-4321-4321-cba987654321",
    "client_id": "12345678-1234-1234-1234-123456789abc",
    "client_secret": "AbC123XyZ789~AbC123XyZ789.AbC123XyZ789",
    "sharepoint_sites": [
        {
            "url": "https://suaempresa.sharepoint.com/sites/site1",
            "nome": "Site de Vendas"
        },
        {
            "url": "https://suaempresa.sharepoint.com/sites/site2",
            "nome": "Site de RH"
        }
    ],
    "onedrive_user_email": "gabrielcarvalho54@empresa.com",
    "backup_base_path": "Backups",
    "onedrive_folder": "Backups_SharePoint",
    "max_backups_to_keep": 7,
    "schedule_time": "02:00"
}
```

---

## ✅ Testar a Configuração

Execute o script para testar:

```bash
python sharepoint_backup_fixed.py
```

Escolha a opção **1** para executar um backup teste.

---

## 🔒 Segurança

### ⚠️ NUNCA faça:
- ❌ Compartilhar o `client_secret`
- ❌ Commitar o `config.json` no Git
- ❌ Enviar por email

### ✅ SEMPRE faça:
- ✅ Adicione `config.json` ao `.gitignore`
- ✅ Use permissões mínimas necessárias
- ✅ Rotacione o secret periodicamente
- ✅ Monitore os logs do Azure AD

---

## 🆘 Solução de Problemas

### Erro: "Insufficient privileges to complete the operation"
**Solução:** Certifique-se de ter clicado em "Grant admin consent"

### Erro: "AADSTS7000215: Invalid client secret is provided"
**Solução:** Verifique se copiou o `client_secret` corretamente (é o "Value", não o "Secret ID")

### Erro: "Resource not found for the segment 'users'"
**Solução:** Adicione a permissão `User.Read.All` no Microsoft Graph

### Erro de conexão ao SharePoint
**Solução:** Verifique se o app tem permissão `Sites.Read.All`

---

## 📞 Recursos Adicionais

- [Documentação Microsoft Graph](https://docs.microsoft.com/en-us/graph/)
- [SharePoint REST API](https://docs.microsoft.com/en-us/sharepoint/dev/sp-add-ins/get-to-know-the-sharepoint-rest-service)
- [Azure AD App Registration](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)

---

**Última atualização:** 2025-10-25
**Versão:** 2.0