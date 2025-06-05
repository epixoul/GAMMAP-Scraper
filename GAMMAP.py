import os

try:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_dir)
    os.system(fr"python {os.getcwd()}" + r"\Scraper.py")
except Exception as e:
    print(e)
