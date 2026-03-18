import paramiko
import sys

def get_forensic_report():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    
    commands = {
        "CORE_HEALTH": "uptime && free -h && df -h && docker ps",
        "ENGAGEMENT_TRIGGERS": "tail -n 50 /root/Active-Defense-Hell/logs/hell_activity.log",
        "CRITICAL_MALWARE": "ls -R /root/Active-Defense-Hell/payloads/ 2>/dev/null | head -n 20 && ls -R /root/Active-Defense-Hell/logs/malware/ 2>/dev/null | head -n 20",
        "CISCO_TRAP_8443": "grep '8443' /root/Active-Defense-Hell/logs/hell_activity.log | tail -n 20",
        "LUCIFER_VOID_REPORT": "tail -n 100 /root/Active-Defense-Hell/logs/lucifer_mini.log"
    }
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password)
        
        report = ""
        for section, cmd in commands.items():
            stdin, stdout, stderr = ssh.exec_command(cmd)
            # Use separate lines to avoid f-string issues if any
            output = stdout.read().decode('utf-8', errors='ignore')
            report += "\n--- " + section + " ---\n"
            report += output + "\n"
            
        ssh.close()
        return report
    except Exception as e:
        return "ERROR_CONEXION: " + str(e)

if __name__ == "__main__":
    print(get_forensic_report())
