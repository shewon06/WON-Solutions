import subprocess

def run_build():
    try:
        # Clear .next cache first
        subprocess.run(["rm", "-rf", ".next"], shell=True)
        # Using powershell to remove if rm fails
        subprocess.run(["powershell", "-Command", "Remove-Item -Path .next -Recurse -Force -ErrorAction SilentlyContinue"], shell=True)
        
        result = subprocess.run(["npm", "run", "build"], capture_output=True, text=True, shell=True)
        print("STDOUT:")
        print(result.stdout[-2000:])
        print("\nSTDERR:")
        print(result.stderr[-2000:])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_build()
