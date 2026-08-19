@echo off
title Suite Sarovi - Automatizacion de Pronosticos
echo ===================================================
echo   🔄 INICIANDO SUITE DE FUTBOL PROFESSIONAL SAROVI  
echo ===================================================
echo.

echo [PASO 1] Ejecutando Raspador Estadistico (API-Football)...
python scraper.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ ERROR: Hubo un problema al ejecutar scraper.py
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [PASO 2] Compilando e Inyectando datos en Plantillas Web...
python generator.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ ERROR: Hubo un problema al ejecutar generator.py
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ===================================================
echo   ✅ PROCESO FINALIZADO CON EXITO BAJO LA MARCA SAROVI
echo ===================================================
echo.
echo 🌐 Iniciando Servidor Web local...
python server.py