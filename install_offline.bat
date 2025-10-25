@echo off
chcp 65001 >nul
cls
echo ========================================================================
echo    Instalando Bibliotecas OFFLINE - SharePoint Backup v4.0
echo ========================================================================
echo.
echo Este script instala as bibliotecas Python a partir dos arquivos
echo baixados na pasta 'portable_libs' (instalação SEM internet)
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
    echo 💡 SOLUÇÃO: Tentando com --user
    pip install --user --no-index --find-links=portable_libs Office365-REST-Python-Client
)
echo.
echo ========================================================================
echo [2/3] Instalando schedule...
echo ========================================================================
pip install --no-index --find-links=portable_libs schedule
if errorlevel 1 (
    pip install --user --no-index --find-links=portable_libs schedule
)
echo.
echo ========================================================================
echo [3/3] Instalando requests...
echo ========================================================================
pip install --no-index --find-links=portable_libs requests
if errorlevel 1 (
    pip install --user --no-index --find-links=portable_libs requests
)
echo.
echo ========================================================================
echo    ✅ Instalação Concluída!
echo ========================================================================
echo.
echo 📝 Próximo passo: Execute executar_backup.bat
echo.
pause