import io
import os
import shutil
import sys
import zipfile
import dotenv
import requests
import win32com.client


def push_env(val, key):
    dotenv.set_key(dotenv.find_dotenv(), val, key)


def find_program_files_dirs():
    inst_env = [
        os.environ.get("ProgramFiles"),
        os.environ.get("ProgramFiles(x86)"),
    ]
    existing = [d for d in inst_env if d and os.path.exists(d)]
    return existing


def inst_setup():
    ext = "\\ESoul\\GAMMAP"
    def_path = find_program_files_dirs()[0] + ext
    inst_dir = input(f"Default path would be: \"{def_path}\""
                     + "\n -Please clarify the installation path,it should be like \"x:\\example0\\example1\""
                     + "\n -or just press \"Enter\": ⤵️"
                     + "\n")
    if inst_dir:
        if not os.path.exists(inst_dir):
            print("❌ The path is invalid.")
            inst_setup()
            return
        else:
            inst_dir = os.path.join(os.path.abspath(inst_dir) + ext)
    else:
        inst_dir = def_path
    print("✅ Destination Folder:" + inst_dir)
    input_val = input("Is it right?(y/n) ")
    if input_val == "y":
        os.makedirs(inst_dir, exist_ok=True)
        push_env("Inst_Path", inst_dir)
    else:
        inst_setup()


def zip_fetch(url, dest_dir):
    zip_response = requests.get(url)
    if zip_response.status_code == 200:
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
            os.mkdir(dest_dir)
        with zipfile.ZipFile(io.BytesIO(zip_response.content)) as zip_file:
            zip_file.extractall(dest_dir)
        for root, dirs, files in os.walk(dest_dir + "\\" + os.listdir(dest_dir)[0]):
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_dir, file)
                if not os.path.exists(dest_file):
                    shutil.move(str(src_file), dest_dir)
        shutil.rmtree(dest_dir + "\\" + os.listdir(dest_dir)[0], ignore_errors=True)


def generate_short(inst_dir):
    try:
        short_path = os.path.join(os.path.expanduser("~"), "Desktop", "GAMMAP.lnk")
        targ_path = inst_dir + r"\source\GAMMAP.py"
        icon_path = inst_dir + r"\source\GAMMAP_ICON.ico"
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(short_path)
        shortcut.TargetPath = targ_path
        shortcut.IconLocation = icon_path
        shortcut.save()
        print("🏷️ The icon has been created.")
    except Exception as e:
        print(e)


def load_up_files(is_update):
    dotenv.load_dotenv()
    dest_dir = os.getenv("Inst_Path") + r"\source"
    if is_update:
        print(f"✅ Source files already exist.")
        print("Updating files...")
    else:
        print("📥 Fetching root files...")
        git = "epixoul"
        repo = "GAMMAP-Scraper"
        api_url = f"https://api.github.com/repos/{git}/{repo}/releases/latest"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                release = response.json()
                zip_url = release["zipball_url"]
                print(f"🆚 Latest release: {release['tag_name']}")
                print(f"📁 Fetching from: {zip_url}")
            if response.status_code != 200:
                print(f"⚠️ Failed to get release info: {response.status_code} Error")
        except Exception:
            print(f"⚠️ Failed to get release info: Problem with connection.")

        try:
            zip_fetch(zip_url, dest_dir)
            print(f"📂 Source files extracted to: {os.path.abspath(dest_dir)}")
        except Exception:
            print(f"🗃️❌ Failed to fetch source zip file.")


def fetch_driver(is_update):
    dotenv.load_dotenv()
    dest_dir = os.getenv("Inst_Path") + r"\drivers"
    driver = os.getenv(f"{os.getenv("Desired_Driver")}")
    if is_update:
        print(f"✅ Driver \"{driver}\" already exist.")
    else:
        shutil.rmtree(dest_dir, ignore_errors=True)
        os.mkdir(dest_dir)
        try:
            print("📥 Fetching driver files...")
            zip_fetch(os.getenv(f"{os.getenv("Desired_Driver")}" + "_Url"), dest_dir)
            print(f"📂 Driver extracted to: {os.path.abspath(dest_dir)}")
        except Exception:
            print(f"🗃️❌ Failed to fetch driver zip file.")


if __name__ == '__main__':
    dotenv.load_dotenv()
    is_update = False
    args = sys.argv[1:]
    if len(args) > 0:
        print("🔼 Running as update:", bool(int(args[1])))
        is_update = bool(int(args[1]))
    inst_setup()
    generate_short(os.getenv("Inst_Path"))
    load_up_files(is_update)
    fetch_driver(is_update)
    input("🦜 Check the \"log_gammap.txt\" file or put comment on e, if any error occurred.")
