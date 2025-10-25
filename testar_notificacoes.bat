@echo off
chcp 65001 >nul
cls
echo ========================================================================
echo    Testar Notificações ntfy.sh - SharePoint Backup v4.0
echo ========================================================================
echo.
echo Este script testa o envio de notificações via ntfy.sh
echo.
set /p TOPIC="Digite seu tópico ntfy (ex: backup-sharepoint-gabrielcarvalho54): "
echo.
echo Enviando notificação de teste para: %TOPIC%
echo.
curl -d "✅ Teste de notificação do SharePoint Backup v4.0 ULTIMATE funcionando!" https://ntfy.sh/%TOPIC%
echo.
echo.
echo ========================================================================
echo Se você recebeu a notificação no seu dispositivo, está funcionando!
echo ========================================================================
echo.
echo 📱 Como receber notificações:
echo   1. Instale o app ntfy no seu celular:
echo      • Android: Play Store - "ntfy"
echo      • iOS: App Store - "ntfy"
echo      • Web: https://ntfy.sh/app
echo.
echo   2. No app, adicione o tópico: %TOPIC%
echo.
echo   3. No arquivo config.json, configure:
echo      "notifications_enabled": true,
echo      "ntfy_topic": "%TOPIC%"
echo.
echo   4. Execute o backup e você receberá notificações de:
echo      • Início do backup
echo      • Avisos e erros
echo      • Conclusão com estatísticas
echo.
echo ⚠️  IMPORTANTE: Use um nome ÚNICO para o tópico!
echo    Evite nomes genéricos como "backup" ou "sharepoint"
echo    Sugestão: backup-sharepoint-seu-nome-empresa-numero
echo.
pause