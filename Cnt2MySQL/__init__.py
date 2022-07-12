from Cnt2MySQL.cnt2mysql_SQLConnector import SQL_Connect
from Cnt2MySQL.cnt2mysql_transform import Transformer
from Cnt2MySQL.cnt2mysql_display import into_html_sentence
from Cnt2MySQL.cnt2mysql_TimeKeeper import TimeKeeper
from colorama import Fore, Back, Style

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

import os
print(f"目前工作目录为：{os.path.abspath(os.curdir)}")

