from time import sleep
import pandas as pd
from typing import *
import webbrowser
import os
from Cnt2MySQL.DefaultHTML import *

def into_html_sentence(tables: Union[List, Tuple], titles: Union[List, Tuple],\
    display_file: str = "tmp.html", leave: bool = False):
    assert tables is not None
    assert len(tables) > 0
    assert len(titles) > 0
    if type(tables[0]) == pd.DataFrame:
        tables = [table.values.tolist() for table in tables]
    
    with open(display_file, "w") as f:
        file_content:List = [DefaultFrame_head]
        navi_content:List = [navi_head]
        arti_content:List = [arti_head]
        
        for i, table in enumerate(tables):
            level = 0
            titles[i] = titles[i].replace("\n", "")
            arti_content.append(("\t"*level)+f"<h1 id=\"{titles[i]}\">{titles[i]}</h1>\n")
            navi_content.append(f"{navi_item[0]}{titles[i]}{navi_item[1]}{titles[i]}{navi_item[2]}")
            if len(table) <= 0:
                arti_content.append(("\t"*level)+"<br />\n")
                continue
            arti_content.append(("\t"*level)+"<table border=\"1\">\n")
            for sub_line in table:
                level += 1
                arti_content.append(("\t"*level)+"<tr>\n")
                for item in sub_line:
                    level += 1
                    arti_content.append(("\t"*level)+f"<td>{item}</td>\n")
                    level -= 1
                arti_content.append(("\t"*level)+"</tr>\n")
                level -= 1
            arti_content.append(("\t"*level)+"</table>\n<br />\n")
        navi_content.append(navi_tail)
        arti_content.append(arti_tail)
        f.writelines(file_content)
        f.writelines(navi_content)
        f.writelines(arti_content)
        f.write(DefaultFrame_tail)
    try:
        webbrowser.open(os.path.abspath(display_file))
        if not leave:
            input(f"按任意键删除{display_file}...")
            os.remove(display_file)
    except:
        print("打开网页失败！")
        
        