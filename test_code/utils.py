import os

class FileHelper:
    def list_files(self, path):
        return os.listdir(path)

def print_hello():
    print("Hello from a safe file!")