import subprocess
import pickle
import io

# Tehlikeli API Anahtarı
SUPER_SECRET_API_KEY = "ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"

# Bariz şifre
password = "admin_password_123!"

def execute_bad_command(command):
    subprocess.run(f"echo {command}", shell=True)

class SecureRunner:
    def run_safe_command(self, command_array):
        subprocess.run(command_array, shell=False)

def deserialize_data(data):
    file_like_object = io.BytesIO(data)
    pickle.load(file_like_object)

execute_bad_command("test")
runner = SecureRunner()
runner.run_safe_command(["ls", "-l"])
deserialize_data(b'\x80\x04K\x01.')