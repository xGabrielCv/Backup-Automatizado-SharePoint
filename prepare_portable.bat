@echo off
chcp 65001 >nul
cls
echo ========================================================================
echo    Preparando Ambiente Portátil - SharePoint Backup v4.0 ULTIMATE
echo ========================================================================
echo.
echo Este script irá:
echo   ✅ Criar estrutura de pastas
echo   ✅ Baixar bibliotecas Python necessárias
echo   ✅ Criar scripts auxiliares para instalação offline
echo.
echo ⚠️  REQUISITOS:
echo   • Python 3.7+ instalado
echo   • Pip funcionando
echo   • Conexão com internet ATIVA
echo.
echo 📦 Bibliotecas que serão baixadas:
echo   • Office365-REST-Python-Client (e dependências)
echo   • schedule
echo   • requests
echo.
pause

echo.
echo ========================================================================
echo [1/6] Criando estrutura de pastas...
echo ========================================================================
if not exist "portable_libs" mkdir portable_libs
if not exist "Backups" mkdir Backups
echo ✅ Pastas criadas: portable_libs, Backups

echo.
echo ========================================================================
echo [2/6] Baixando Office365-REST-Python-Client...
echo ========================================================================
echo (Isso pode demorar vários minutos dependendo da sua conexão)
echo.
pip download Office365-REST-Python-Client -d portable_libs
if errorlevel 1 (
    echo ❌ Erro ao baixar Office365-REST-Python-Client
    pause
    exit /b 1
)
echo ✅ Office365-REST-Python-Client baixado

echo.
echo ========================================================================
echo [3/6] Baixando schedule...
echo ========================================================================
pip download schedule -d portable_libs
if errorlevel 1 (
    echo ❌ Erro ao baixar schedule
    pause
    exit /b 1
)
echo ✅ schedule baixado

echo.
echo ========================================================================
echo [4/6] Baixando requests...
echo ========================================================================
pip download requests -d portable_libs
if errorlevel 1 (
    echo ❌ Erro ao baixar requests
    pause
    exit /b 1
)
echo ✅ requests baixado

echo.
echo ========================================================================
echo [5/6] Criando scripts auxiliares...
echo ========================================================================

REM ============================================================================
REM Criar install_offline.bat
REM ============================================================================
(
echo @echo off
echo chcp 65001 ^>nul
echo cls
echo ========================================================================
echo    Instalando Bibliotecas OFFLINE - SharePoint Backup v4.0
echo ========================================================================
echo.
echo Este script instala as bibliotecas Python a partir dos arquivos
echo baixados na pasta 'portable_libs' (instalação SEM internet^)
echo.
echo ⚠️  Execute este script APENAS se:
echo   • Você está em um PC SEM acesso à internet
echo   • A pasta portable_libs contém os arquivos .whl
echo.
pause
echo.
echo ========================================================================
echo [1/3] Instalando Office365-REST-Python-Client...
echo ========================================================================
pip install --no-index --find-links=portable_libs Office365-REST-Python-Client
if errorlevel 1 (
    echo ❌ Erro ao instalar Office365-REST-Python-Client
    echo.
    echo 💡 SOLUÇÃO: Tente com --user
    pip install --user --no-index --find-links=portable_libs Office365-REST-Python-Client
^)
echo.
echo ========================================================================
echo [2/3] Instalando schedule...
echo ========================================================================
pip install --no-index --find-links=portable_libs schedule
if errorlevel 1 (
    pip install --user --no-index --find-links=portable_libs schedule
^)
echo.
echo ========================================================================
echo [3/3] Instalando requests...
echo ========================================================================
pip install --no-index --find-links=portable_libs requests
if errorlevel 1 (
    pip install --user --no-index --find-links=portable_libs requests
^)
echo.
echo ========================================================================
echo    ✅ Instalação Concluída!
echo ========================================================================
echo.
echo 📝 Próximo passo: Execute executar_backup.bat
echo.
pause
) > install_offline.bat

REM ============================================================================
REM Criar executar_backup.bat
REM ============================================================================
(
echo @echo off
echo chcp 65001 ^>nul
echo cls
echo ========================================================================
echo    Sistema de Backup Automatizado SharePoint v4.0 ULTIMATE
echo    Autor: gabrielcarvalho54
echo    Data: 2025-10-25
echo ========================================================================
echo.
python sharepoint_backup_ultimate.py
echo.
echo ========================================================================
echo.
pause
) > executar_backup.bat

REM ============================================================================
REM Criar verificar_instalacao.bat
REM ============================================================================
(
echo @echo off
echo chcp 65001 ^>nul
echo cls
echo ========================================================================
echo    Verificando Instalação - SharePoint Backup v4.0
echo ========================================================================
echo.
echo [1/4] Verificando Python...
python --version
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo    Instale Python 3.7+ de: https://www.python.org/downloads/
    pause
    exit /b 1
^)
echo ✅ Python OK
echo.
echo [2/4] Verificando pip...
pip --version
if errorlevel 1 (
    echo ❌ pip não encontrado!
    pause
    exit /b 1
^)
echo ✅ pip OK
echo.
echo [3/4] Verificando bibliotecas instaladas...
echo.
echo Procurando Office365-REST-Python-Client:
pip show Office365-REST-Python-Client
echo.
echo Procurando schedule:
pip show schedule
echo.
echo Procurando requests:
pip show requests
echo.
echo [4/4] Verificando arquivos do projeto...
if exist "sharepoint_backup_ultimate.py" (
    echo ✅ sharepoint_backup_ultimate.py encontrado
^) else (
    echo ❌ sharepoint_backup_ultimate.py NÃO encontrado!
^)
if exist "config.json" (
    echo ✅ config.json encontrado
^) else (
    echo ⚠️  config.json não encontrado (será criado na primeira execução^)
^)
if exist "portable_libs" (
    echo ✅ portable_libs/ encontrado
^) else (
    echo ⚠️  portable_libs/ não encontrado
^)
echo.
echo ========================================================================
echo    Verificação concluída!
echo ========================================================================
pause
) > verificar_instalacao.bat

REM ============================================================================
REM Criar testar_notificacoes.bat
REM ============================================================================
(
echo @echo off
echo chcp 65001 ^>nul
echo cls
echo ========================================================================
echo    Testar Notificações ntfy.sh
echo ========================================================================
echo.
echo Este script testa o envio de notificações via ntfy.sh
echo.
set /p TOPIC="Digite seu tópico ntfy (ex: backup-sharepoint-seu-nome): "
echo.
echo Enviando notificação de teste para: %TOPIC%
echo.
curl -d "Teste de notificação do SharePoint Backup v4.0" https://ntfy.sh/%TOPIC%
echo.
echo.
echo ========================================================================
echo Se você recebeu a notificação no seu dispositivo, está funcionando!
echo ========================================================================
echo.
echo 📱 Como receber notificações:
echo   1. Instale o app ntfy no seu celular (Android/iOS^)
echo   2. Adicione o tópico: %TOPIC%
echo   3. Configure no config.json:
echo      "notifications_enabled": true,
echo      "ntfy_topic": "%TOPIC%"
echo.
pause
) > testar_notificacoes.bat

echo ✅ Scripts auxiliares criados:
echo    • install_offline.bat
echo    • executar_backup.bat
echo    • verificar_instalacao.bat
echo    • testar_notificacoes.bat

echo.
echo ========================================================================
echo [6/6] Contando arquivos baixados...
echo ========================================================================
dir /b portable_libs\*.whl | find /c ".whl"
echo arquivos .whl baixados em portable_libs/
echo.

echo ========================================================================
echo    ✅ PREPARAÇÃO CONCLUÍDA COM SUCESSO!
echo ========================================================================
echo.
echo 📦 Estrutura criada:
echo    SharePoint_Backup/
echo    ├── sharepoint_backup_ultimate.py   (script principal^)
echo    ├── config.json                      (configuração^)
echo    ├── portable_libs/                   (bibliotecas Python^)
echo    ├── install_offline.bat              (instalador offline^)
echo    ├── executar_backup.bat              (atalho execução^)
echo    ├── verificar_instalacao.bat         (verificar ambiente^)
echo    └── testar_notificacoes.bat          (testar ntfy^)
echo.
echo 📝 PRÓXIMOS PASSOS:
echo.
echo 1️⃣  Configure o arquivo config.json:
echo    • Adicione suas credenciais do Azure AD
echo    • Configure URLs dos sites SharePoint
echo    • Configure email do OneDrive
echo    • (Opcional^) Ative notificações
echo.
echo 2️⃣  Para usar em MODO PORTÁTIL (pendrive^):
echo    a^) Copie TODA esta pasta para o pendrive
echo    b^) No PC da empresa (sem internet^):
echo       - Execute: install_offline.bat
echo       - Depois: executar_backup.bat
echo.
echo 3️⃣  Para usar em MODO LOCAL (este PC^):
echo    a^) Se tem internet:
echo       - Execute: pip install Office365-REST-Python-Client schedule requests
echo       - Depois: executar_backup.bat
echo    b^) Se NÃO tem internet:
echo       - Execute: install_offline.bat
echo       - Depois: executar_backup.bat
echo.
echo 4️⃣  (Opcional^) Testar notificações:
echo    - Execute: testar_notificacoes.bat
echo.
echo ========================================================================
echo.
pause