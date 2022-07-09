from time import sleep
import pandas as pd
from typing import *
import webbrowser
import os
import re
from Cnt2MySQL.DefaultHTML import *

# 网页框架设置器
class WebPageSetter:
    def __init__(self, col: int = 2, default_html: Sequence = [DefaultFrame_tail, DefaultFrame_head]):# 注意，default_html中tail在前
        """
        初始化设置器

        Args:
            col (int, optional): 一共有几个子框架. Defaults to 2.
            default_html (Sequence, optional): 文件整体的头尾部，一般是固定的（HTML头部和尾部）. Defaults to [DefaultFrame_tail, DefaultFrame_head].
        """
        assert col >= 1
        assert len(default_html) >= 2
        # 所有子框架的集合，第一个元素是整体文件头尾部
        self.file_content: List[Sequence] = [default_html]+[[] for _ in range(col)] 
        self.column_n:int = col

    def set_CSS_style(self, CSS_style: str, outer_CSS_style: str = ""):
        """
        设置CSS样式

        Args:
            CSS_style (str): 内部CSS样式
            outer_CSS_style (str, optional): 外部文件链接，最好不是本地文件. Defaults to "".
        """
        
        # 正则表达式
        #内部链接
        pat1 = re.compile(r"[\s\S]*(</style>)[\s\S]*")
        #外部链接
        pat2 = re.compile(r"[\s\S]*(</head>)[\s\S]*")
        res1 = pat1.match(self.file_content[0][0])
        if res1 is not None:
            pat1.sub(res1.group(1), CSS_style+"</style>")
        else:
            pat2.sub(pat2.match(self.file_content[0][0]).group(
                1), CSS_style+"</head>")
        # 如果有外部链接就设置外部链接
        if outer_CSS_style != "":
            pat2.sub(pat2.match(self.file_content[0][0]).group(
                1), outer_CSS_style+"</head>")

    def set_JS_script(self, JS_script: str, outer_JS_script: str = ""):
        """
        设置JS脚本

        Args:
            JS_script (str): 内部脚本
            outer_JS_script (str, optional): 外部链接. Defaults to "".
        """
        pat1 = re.compile(r"[\s\S]*(</script>)[\s\S]*")
        pat2 = re.compile(r"[\s\S]*(</head>)[\s\S]*")
        res1 = pat1.match(self.file_content[0][0])
        if res1 is not None:
            pat1.sub(res1.group(1), JS_script+"</script>")
        else:
            pat2.sub(pat2.match(self.file_content[0][0]).group(
                1), JS_script+"</head>")
        if outer_JS_script != "":
            pat2.sub(pat2.match(self.file_content[0][0]).group(
                1), outer_JS_script+"</head>")

    def set_frame(self, head: str, tail: str, frame_to_set: int = 1):
        """
        初始化子框架头尾部

        Args:
            head (str): 子框架头部
            tail (str): 子框架尾部
            frame_to_set (int, optional): 哪一个子框架. Defaults to 1.
        """
        #将尾部放在首位
        self.file_content[frame_to_set] = [tail, head]

    def add_to_frame(self, content: str, frame_to_add: int = 1, head: str = '', tail: str = ''):
        """
        在子框架中添加元素

        Args:
            content (str): 元素内容
            frame_to_add (int, optional): 哪一个子框架. Defaults to 1.
            head (str, optional): 内容的头部. Defaults to ''.
            tail (str, optional): 内容的尾部. Defaults to ''.
        """
        self.file_content[frame_to_add].append(head + content + tail)

    def write_into_html_file(self, filename: str = "tmp.html", mode: str = "w"):
        """
        写入HTML文档

        Args:
            filename (str, optional): HTML文件名. Defaults to "tmp.html".
            mode (str, optional): 文件读写模式. Defaults to "w".
        """
        with open(filename, mode) as f:
            for item in self.file_content:
                f.writelines(item[1:])
                # 尾部在首位，最后再加上
                f.write(item[0])


def set_table_content(table: Union[List, Tuple], table_content: List[str], header: str = ""):
    """
    将二维列表转HTML表格

    Args:
        table (Union[List, Tuple]): 表格的列表形式
        table_content (List[str]): 要将转换后的HTML语句放入的列表（该列表为所有表格HTML语句的集合）
        header (str, optional): 每个列表的标题. Defaults to "".
    """
    table_content.append(header)
    # level:缩进个数
    level = 0
    table_content[-1] += ("\t"*level)+"<table>\n<br />\n"
    for sub_line in table:
        level += 1
        table_content[-1] += ("\t"*level)+"<tr>\n"
        # 设置单个表格单元
        for item in sub_line:
            level += 1
            table_content[-1] += ("\t"*level)+f"<td>{item}</td>\n"
            level -= 1
        table_content[-1] += ("\t"*level)+"</tr>\n"
        level -= 1
    table_content[-1] += ("\t"*level)+"</table>\n<br />\n"
def into_html_sentence(tables: Union[List, Tuple], titles: Sequence,\
    display_file: str = "tmp.html", leave: bool = False):
    """
    将表格转换为HTML语句

    Args:
        tables (Union[List, Tuple]): 表格的python表示
        titles (Sequence): 各个表格的标题（SQL语句）
        leave (bool, optional): 是否保留生成的HTML文件. Defaults to False.
    """
    assert tables is not None
    assert len(tables) > 0
    assert len(titles) > 0
    # 将DataFrame转为列表
    if type(tables[0]) == pd.DataFrame:
        tables = [table.values.tolist() for table in tables]
    # 初始化设置器
    setter = WebPageSetter()
    #初始化子框架
    setter.set_frame(navi_head, navi_tail)
    setter.set_frame(arti_head, arti_tail, 2)
    arti_content = []
    for i, table in enumerate(tables):
        # 设置索引
        titles[i] = titles[i].replace("\n", "")
        setter.add_to_frame(titles[i], 1, navi_item[0]+titles[i]+navi_item[1], navi_item[2])
        set_table_content(table, arti_content, f"<h1 id=\"{titles[i]}\">{titles[i]}</h1>\n")
    # 设置正文内容
    setter.add_to_frame("\n".join(arti_content), 2)
    setter.write_into_html_file() 
    # 通过浏览器打开
    try:
        webbrowser.open(os.path.abspath(display_file))
        # 如果函数传入参数leave=True，那么显示完结果后HTML文件不会删除
        if not leave:
            input(f"按任意键删除{display_file}...")
            os.remove(display_file)
    except:
        print("打开网页失败！")
        
        