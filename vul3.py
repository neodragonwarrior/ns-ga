import subprocess

def run_system_command(command):
    subprocess.call(command, shell=True)  # Potential command injection

