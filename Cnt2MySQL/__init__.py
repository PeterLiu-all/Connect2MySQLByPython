import os
from Cnt2MySQL.cnt2mysql_SQLConnector import SQLConnect
from Cnt2MySQL.cnt2mysql_transform import Transformer
from Cnt2MySQL.cnt2mysql_display import into_html_sentence
from Cnt2MySQL.cnt2mysql_interactive import InteractiveSQLConnect
from colorama import Fore, Back, Style
from sys import executable
# 打印logo
print(Fore.CYAN + Style.DIM)
print('''
 ______                            __ ___   __  ___     _____ ____    __ 
  / ____/___  ____  ____  ___  _____/ /|__ \ /  |/  /_  _/ ___// __ \  / / 
 / /   / __ \/ __ \/ __ \/ _ \/ ___/ __/_/ // /|_/ / / / |__ \/ / / / / /  
/ /___/ /_/ / / / / / / /  __/ /__/ /_/ __// /  / / /_/ /__/ / /_/ / / /___
\____/\____/_/ /_/_/ /_/\___/\___/\__/____/_/  /_/\__, /____/\___\_\/_____/
                                                 /____/                    
              ''')
print(Style.RESET_ALL)

print(f"目前工作目录为：{os.path.abspath(os.curdir)}")
print(f"当前解释器地址：{executable}")
