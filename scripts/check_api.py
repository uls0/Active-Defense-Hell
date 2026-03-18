import paramiko

def check_api_and_logs():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, port, user, password)
        
        # Test API
        stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:8888/api/stats")
        api_res = stdout.read().decode()
        
        # Test Logs
        stdin, stdout, stderr = ssh.exec_command("tail -n 20 /root/Active-Defense-Hell/logs/hell_activity.log")
        log_res = stdout.read().decode()
        
        print("API_OUT:" + api_res)
        print("LOG_OUT:" + log_res)
        
        ssh.close()
    except Exception as e:
        print("Error:" + str(e))

if __name__ == "__main__":
    check_api_and_logs()
