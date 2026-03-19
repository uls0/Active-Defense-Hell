# TITAN_OS DECEPTION SCRIPT - v17.1
# Goal: Waste attacker time and plant canaries

$Desktop = "C:\Users\Public\Desktop"

# 1. Create Folder Maze (1000 items)
for ($i=1; $i -le 100; $i++) {
    $base = Join-Path $Desktop "BACKUP_SYSTEM_v$i"
    New-Item -ItemType Directory -Path $base -Force | Out-Null
    for ($j=1; $j -le 10; $j++) {
        $sub = Join-Path $base "CONFIG_DATA_$j"
        New-Item -ItemType Directory -Path $sub -Force | Out-Null
        New-Item -ItemType File -Path (Join-Path $sub "Secret_Keys.txt") -Value "REDACTED_ACCESS_TOKEN_0x8888" | Out-Null
    }
}

# 2. Plant Canary Tokens (Simulated)
New-Item -ItemType File -Path (Join-Path $Desktop "VPN_CREDENTIALS_PROD.txt") -Value "User: sysadmin | Pass: Winter2026!" | Out-Null
New-Item -ItemType File -Path (Join-Path $Desktop "URGENT_DB_SYNC.docx") -Value "This is a monitored file. Access has been logged." | Out-Null

# 3. Create Junk Data
$LargeFile = "C:\Users\Public\Documents\NTDS_BACKUP.dat"
fsutil file createnew $LargeFile 524288000 # 500MB Real Junk
