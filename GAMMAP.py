import os
import sys

try:
    current_dir = sys.path[0]
    os.system(fr"python {current_dir}" + r"\Scraper.py")
except Exception as e:
    print(e)
