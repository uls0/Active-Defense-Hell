import sys
sys.path.append('scripts')
import threat_intel
import os
ip = '18.144.24.239'
key = os.getenv('VT_API_KEY')
comment = 'HELL SENTINEL: High-priority detection of Aeternum C2 botnet node. Targeted port 18080 (Monero P2P). Host identified as persistent crypto-attacker. Location: San Jose, US.'
print(f'Reporting {ip}...')
result = threat_intel.report_ip_to_vt(ip, key, comment)
print(f'Result: {result}')
