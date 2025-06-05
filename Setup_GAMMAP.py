import ctypes
import subprocess
import sys
import os
import threading


def requirements(file):
    if not os.path.exists(file):
        print(f"❌ '{file}' file not found.")
        sys.exit(1)

    print(f"📦 Installing packages from '{file}'...\n")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", file])
        print("\n✅ All packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Installation failed: {e}")


def run_asadmin(is_update):
    script = os.path.dirname(os.path.realpath(__file__)) + r"\Ctr_GAMMAP.py"
    prams = ''.join([script] + sys.argv[1:] + [' asadmin'] + [f' {is_update}'])
    ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, prams, None, 1)


if __name__ == "__main__":
    requirements(r"requirements.txt")
    run_asadmin(0)