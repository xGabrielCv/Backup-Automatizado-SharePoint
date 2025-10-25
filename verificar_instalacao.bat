@echo off
chcp 65001 >nul
cls
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
)
echo ✅ Python OK
echo.
echo [2/4] Verificando pip...
pip --version
if errorlevel 1 (
    echo ❌ pip não encontrado!
    pause
    exit /b 1
)
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
) else (
    echo ❌ sharepoint_backup_ultimate.py NÃO encontrado!
)
if exist "config.json" (
    echo ✅ config.json encontrado
) else (
    echo ⚠️  config.json não encontrado (será criado na primeira execução)
)
if exist "portable_libs" (
    echo ✅ portable_libs/ encontrado
) else (
    echo ⚠️  portable_libs/ não encontrado
)
echo.
echo ========================================================================
echo    Verificação concluída!
echo ========================================================================
pause