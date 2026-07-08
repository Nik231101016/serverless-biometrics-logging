import os
import sys
import paramiko

# Read environment variables injected securely by GitHub Secrets
EC2_HOST = os.environ.get("EC2_HOST")
EC2_USERNAME = os.environ.get("EC2_USERNAME", "ec2-user")
# GitHub actions passes the secret key value as a multi-line string
SSH_PRIVATE_KEY_DATA = os.environ.get("PRIVATE_KEY")

if not EC2_HOST or not SSH_PRIVATE_KEY_DATA:
    print("🛑 Deployment Configuration Fault: Missing Environment Secrets.")
    sys.exit(1)

print(f"🚀 Initializing secure SSH connection loop to: {EC2_HOST}")

try:
    # Set up Paramiko SSH Client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Load the private key string data directly from environment memory
    pkey_io = paramiko.RSAKey.from_private_key_list(SSH_PRIVATE_KEY_DATA.splitlines())
    
    # Connect to remote target host
    client.connect(
        hostname=EC2_HOST,
        username=EC2_USERNAME,
        pkey=pkey_io,
        timeout=15
    )
    
    print("🟢 SSH Authentication Succeeded. Executing remote cloud deployment sequence...")
    
    # Sequential commands to pull down adjustments and run app
    commands = [
        "cd /home/ec2-user/project",
        "git pull origin main || (git clone https://github.com/Nik231101016/aws-python-deployment-demo.git .)",
        "python3 app.py"
    ]
    
    for command in commands:
        print(f"⚙️ Running: {command}")
        stdin, stdout, stderr = client.exec_command(command)
        
        # Read execution returns
        output = stdout.read().decode().strip()
        errors = stderr.read().decode().strip()
        
        if output:
            print(output)
        if errors and "error" in errors.lower():
            print(f"⚠️ Warning/Error: {errors}")

    client.close()
    print("✅ Deployment Completed Successfully! Pipeline Nominal.")

except Exception as e:
    print(f"🛑 Critical System Deployment Crash: {str(e)}")
    sys.exit(1)
