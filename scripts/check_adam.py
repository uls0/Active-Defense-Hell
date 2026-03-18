import paramiko

def debug_magi():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    
    commands = {
        "DASHBOARD_RUNTIME_LOGS": "docker logs hell_dashboard --tail 20",
        "LOG_FILE_TAIL": "tail -n 20 /root/Active-Defense-Hell/logs/hell_activity.log",
        "NETSTAT_CHECK": "netstat -tulnp | grep -E '8888|3389|502|102|22|80|443'",
        "DOCKER_PS": "docker ps --format 'table {{.Names}}\t{{.Status}}'"
    }
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password)
        
        for name, cmd in commands.items():
            print(f"\n=== {name} ===")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(stdout.read().decode('utf-8'))
            print(stderr.read().decode('utf-8'))
            
        ssh.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    debug_magi()
