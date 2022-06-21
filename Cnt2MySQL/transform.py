from typing import Callable, Dict, List
import pandas
import mistune
import os
import re
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


class Transformer:
    def __init__(self, dataframes: List[pandas.DataFrame], name: str = "transform", direc: str = ".") -> None:
        """初始化

        Args:
            dataframes (list[pandas.DataFrame]): 想要转换的表格列表
            name (str, optional): 转换后的文件名（不含后缀名）. Defaults to "transform".
            direc (str, optional): 路径名. Defaults to ".".
        """
        self.dataframes: List[pandas.DataFrame] = dataframes
        self.name: str = name
        self.pname: str = os.path.join(direc, name)
        self.direc: str = direc

    def __NormalModule(self, func: Callable, ext: str) -> None:
        """模板

        Args:
            func (Callable): 使用的函数
            ext (str): 后缀名
        """
        for i in range(len(self.dataframes)):
            df = self.dataframes[i]
            func(df, f"{self.pname}{i+1}"+ext)

    def to_pdf(self) -> None:
        for i in range(len(self.dataframes)):
            df = self.dataframes[i]
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.axis('tight')
            ax.axis('off')
            the_table = ax.table(cellText=df.values,
                                 colLabels=df.columns, loc='center')
            pp = PdfPages(f"{self.pname}{i}.pdf")
            pp.savefig(fig, bbox_inches='tight')
            pp.close()

    def to_img(self) -> None:
        for i in range(len(self.dataframes)):
            df = self.dataframes[i]
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.axis('tight')
            ax.axis('off')
            the_table = ax.table(cellText=df.values,
                                 colLabels=df.columns, loc='center')
            plt.savefig(f"{self.pname}{i}.png")

    def to_markdown(self) -> None:
        self.__NormalModule(pandas.DataFrame.to_markdown, ".md")

    def to_html(self) -> None:
        Default_CSS:str = '''
<style>
    table{
        width: fit-content;
        height: auto;
        font-size: larger;
        font-family: 'Lucida Console',楷体, 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        font-weight: bold;
        background-color: rgba(245, 245, 245, 0.7);
        padding: 0;
        margin: auto;
        border-width: 0;
        outline-style: solid;
        outline-color: rgba(2, 2, 2, 0.7);
    }
    tr{
    padding: 0;
    margin: 0;
    border-color: rgba(170, 170, 170, 0.4);
    }
    td{
        padding: 10px;
        margin: 0;
        font-size: large;
        text-align: right;
        border-color: rgba(170, 170, 170, 0.4);
    }
</style>\n
        '''
        def default_to_html(df:pandas.DataFrame, name:str):
            df.to_html(name)
            with open(name, "r") as f:
                file_content = Default_CSS+f.read()
            with open(name, "w") as f:
                f.write(f"{file_content}\n\n")
        self.__NormalModule(default_to_html, ".html")

    def to_csv(self) -> None:
        self.__NormalModule(pandas.DataFrame.to_csv, ".csv")

    def to_excel(self) -> None:
        self.__NormalModule(pandas.DataFrame.to_excel, ".xlsx")

    def to_txt(self)->None:
        def write_to_txt(df: pandas.DataFrame, name:str):
            df_str:Dict = df.to_string()
            with open(name, "w") as f:
                f.write(f"{df_str}\n\n")
        self.__NormalModule(write_to_txt, ".txt")
    def to_all(self) -> None:
        """转换为可用的所有格式
        """
        self.to_csv()
        self.to_excel()
        self.to_html()
        self.to_img()
        self.to_markdown()
        self.to_pdf()
        self.to_txt()


def clean_all(name: str = "transform", direc: str = ".") -> bool:
    jud: bool = False
    pat: re.Pattern = re.compile(name+r"[0-9]*\.(?!py)(.*)")
    for f in os.listdir(direc):
        if re.match(pat, f) is not None:
            os.remove(os.path.join(direc, f))
            jud = True
    return jud
