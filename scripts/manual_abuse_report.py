import sys
sys.path.append('scripts')
import abuse_api
import os
ip = '4.17.226.146'
comment = 'HELL ACTIVE DEFENSE: Massive exfiltration attempt detected (139MB). Persistent bot trapped in Hydra-Gorgon loop. Cumulative time secured: 5000s+. High-confidence botnet node.'
print(f'Reporting {ip} to AbuseIPDB...')
result = abuse_api.report_ip(ip, '14,15', comment)
print(f'Result: {result}')
