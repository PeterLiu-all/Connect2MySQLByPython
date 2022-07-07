from time import sleep
import pandas as pd
from typing import *
import webbrowser
import os
from Cnt2MySQL.DefaultCSS import Default_CSS

def into_html_sentence(tables: Union[List, Tuple], titles: Union[List, Tuple],\
    display_file: str = "tmp.html", leave: bool = False):
    assert tables is not None
    assert len(tables) > 0
    assert len(titles) > 0
    if type(tables[0]) == pd.DataFrame:
        tables = [table.values.tolist() for table in tables]
    
    with open(display_file, "w") as f:
        f.write(Default_CSS)
        for i, table in enumerate(tables):
            level = 0
            f.write(("\t"*level)+f"<h1>{titles[i]}</h1>\n")
            if len(table) <= 0:
                f.write(("\t"*level)+"<br />\n")
                continue
            f.write(("\t"*level)+"<table border=\"1\">\n")
            for sub_line in table:
                level += 1
                f.write(("\t"*level)+"<tr>\n")
                for item in sub_line:
                    level += 1
                    f.write(("\t"*level)+f"<td>{item}</td>\n")
                    level -= 1
                f.write(("\t"*level)+"</tr>\n")
                level -= 1
            f.write(("\t"*level)+"</table>\n<br />\n")
    try:
        webbrowser.open(os.path.abspath(display_file))
        if not leave:
            input(f"按任意键删除{display_file}...")
            os.remove(display_file)
    except:
        print("打开网页失败！")
        
        