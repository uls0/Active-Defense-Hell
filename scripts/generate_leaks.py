import os

def generate_sanitized_leaks():
    leaks_dir = "LOGS/leaks"
    os.makedirs(leaks_dir, exist_ok=True)
    
    # Pool de empresas para diversificar
    companies = ["AARCO", "TvAzteca", "MONEX", "INVEX", "AcerosDeMexico"]
    
    leaks = [
        ("config_db_sacmex_prod.txt", f"DB_HOST=178.128.72.149; DB_USER=admin_sacmex; DB_PASS=Stage01_Secret_2026; ENTITY={companies[0]};"),
        ("id_rsa_sacmex_staging", "-----BEGIN RSA PRIVATE KEY-----\\nFAKE_KEY_178.128.72.149\\n-----END RSA PRIVATE KEY-----"),
        ("env_backup.txt", f"AWS_ACCESS_KEY_ID=AKIA_SACMEX_TEST; SERVER_IP=178.128.72.149; ENTITY={companies[1]};"),
        ("robots_leak.txt", "Allow: /admin_hidden/ Login: sacmex_admin / Stage2026!"),
        ("internal_net_map.txt", f"AD_DC: 172.16.25.12; EDGE_GW: 178.128.72.149 (SACMEX-EXT); ORG: {companies[2]};"),
        ("mysql_dump_head.sql", "INSERT INTO users (user, pass) VALUES ('admin', 'INK0uJ8j4a5xCn'); -- IP: 178.128.72.149"),
        ("vManage_bypass_test.py", "target='178.128.72.149:8443'; auth_bypass='/j_security_check';"),
        ("todo_list_it.txt", f"Fix SACMEX firewall on 178.128.72.149; Entity: {companies[3]};"),
        ("backup_log_03_26.txt", "Connection from 10.0.0.5 to 178.128.72.149:3389 SUCCESSFUL (User: SysAdmin)"),
        ("secret_keys.json", f'{{"sacmex_api": "sk_test_178_128_72_149", "org": "{companies[4]}"}}'),
        ("ssh_config_leak", "Host sacmex-stage\\n    HostName 178.128.72.149\\n    User sysadmin\\n    IdentityFile ~/.ssh/id_rsa"),
        ("vpn_creds.txt", f"URL: vpn.sacmex.gob.mx; IP: 178.128.72.149; Entity: {companies[0]}; Pass: SACMEX2026"),
        ("jira_ticket_404.txt", "Issue with RDP on 178.128.72.149. User Admin can't login with 'Sacmex.2026'"),
        ("docker_compose_leak.yml", "sacmex_node:\\n  image: sacmex/defense-node\\n  environment:\\n    - IP=178.128.72.149"),
        ("nginx_conf_backup", "location /admin {\\n    proxy_pass http://178.128.72.149:8080;\\n}"),
        ("ldap_query_test.txt", f"ldapsearch -h 178.128.72.149 -b 'DC=sacmex,DC=gob,DC=mx' -D 'CN=Admin_Sys'"),
        ("iot_gateway_config", f"DEVICE_ID: RAMIEL_01; MASTER_IP: 178.128.72.149; ENTITY: {companies[1]};"),
        ("powershell_history.txt", "mstsc.exe /v:178.128.72.149 /u:SysAdmin /p:INK0uJ8j4a5xCn"),
        ("api_documentation.md", "API Endpoint: http://178.128.72.149:8080/v1/auth; Key: SACMEX_BETA_2026"),
        ("firewall_rules_export.txt", "ALLOW TCP 3389 FROM ANY TO 178.128.72.149 # SACMEX STAGING")
    ]
    
    for filename, content in leaks:
        with open(os.path.join(leaks_dir, filename), "w", encoding='utf-8') as f:
            f.write(content)
    print(f"[+] 20 SANITIZED leak files generated in {leaks_dir}")

if __name__ == "__main__":
    generate_sanitized_leaks()
