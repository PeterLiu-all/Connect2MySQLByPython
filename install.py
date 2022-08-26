from sys import executable
import shutil
import platform
from os import system, path

sep = path.sep

system("pip install -r requirements.txt")
input("按任意键以继续...")
system("pyinstaller -F Cnt2MySQLInteractive.py -n cnt2mysql")
input("按任意键以继续...")
system("conda deactivate")
input("按任意键以继续...")

if platform.system() == "Linux":
    system("sudo mv ./dist/cnt2mysql /usr/local/bin/")
else:
    shutil.move("." + sep + "dist" + sep + "cnt2mysql" + path.splitext(executable)[-1], path.dirname(executable))
