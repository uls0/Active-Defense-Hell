import paramiko
import json

def forensic_audit():
    nodes = {
        "PRO": ("178.128.72.149", 2200, "INK0uJ8j4a5xCn"),
        "SEC": ("170.64.151.185", 22, "INK0uJ8j4a5xCR")
    }
    
    results = {}
    for name, (host, port, pwd) in nodes.items():
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, "root", pwd, timeout=15)
            
            commands = {
                "total_hits": "wc -l /root/Active-Defense-Hell/logs/hell_activity.log",
                "void_trapped": "grep 'Port: 6666' /root/Active-Defense-Hell/logs/hell_activity.log | wc -l",
                "fifield_dispatched": "grep '💣 LETHAL_INJECTION' /root/Active-Defense-Hell/logs/hell_activity.log | wc -l",
                "exfil_maze_engaged": "grep '📦 EXFIL_START' /root/Active-Defense-Hell/logs/hell_activity.log | wc -l",
                "top_aggressors": "awk -F'IP:' '{print $2}' /root/Active-Defense-Hell/logs/hell_activity.log | awk -F'|' '{print $1}' | sort | uniq -c | sort -nr | head -n 5",
                "ransom_notes_blocked": "grep '🚨 RANSOM_NOTE' /root/Active-Defense-Hell/logs/hell_activity.log | wc -l"
            }
            
            node_report = {}
            for key, cmd in commands.items():
                stdin, stdout, stderr = ssh.exec_command(cmd)
                node_report[key] = stdout.read().decode('utf-8').strip()
            
            results[name] = node_report
            ssh.close()
        except Exception as e:
            results[name] = {"error": str(e)}
            
    return results

if __name__ == "__main__":
    report = forensic_audit()
    print(json.dumps(report, indent=2))
