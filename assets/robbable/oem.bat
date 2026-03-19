@echo off
echo [*] TITAN_OS LEGACY DECEPTION ACTIVATED
echo [*] Setting up Sacrifice Environment...

:: 1. Crear Laberinto de Carpetas (Legacy Style)
cd C:\Documents and Settings\All Users\Desktop
mkdir BACKUP_SISTEMA_CONTABLE
cd BACKUP_SISTEMA_CONTABLE
for /L %%i in (1,1,50) do (
    mkdir DATA_VOL_%%i
    echo 0x8888_SECRET_TOKEN_REDACTED > DATA_VOL_%%i\keys_%%i.txt
)

:: 2. Plantar Archivos de Alta Atracción
echo AD_ADMIN: Admin1234! > "C:\Documents and Settings\All Users\Desktop\PASSWORDS_DC_2026.txt"
echo VPN_GATEWAY: 201.151.93.114 >> "C:\Documents and Settings\All Users\Desktop\PASSWORDS_DC_2026.txt"

:: 3. Simular Archivos de Sistema Sensibles
mkdir C:\AD_STAGING
echo [DB_BACKUP_MARKER] > C:\AD_STAGING
tds.dit
fsutil file createnew C:\AD_STAGING\large_log.dat 104857600

echo [OK] Deception ready for engagement.
