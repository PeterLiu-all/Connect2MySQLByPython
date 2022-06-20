from typing import Callable, List
import pandas
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
        self.dataframes: list[pandas.DataFrame] = dataframes
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
            func(df, f"{self.pname}{i}"+ext)

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
        self.__NormalModule(pandas.DataFrame.to_html, ".html")

    def to_csv(self) -> None:
        self.__NormalModule(pandas.DataFrame.to_csv, ".csv")

    def to_excel(self) -> None:
        self.__NormalModule(pandas.DataFrame.to_excel, ".xlsx")

    def to_all(self) -> None:
        """转换为可用的所有格式
        """
        self.to_csv()
        self.to_excel()
        self.to_html()
        self.to_img()
        self.to_markdown()
        self.to_pdf()


def clean_all(name: str = "transform", direc: str = ".") -> bool:
    jud: bool = False
    pat: re.Pattern = re.compile(name+r"[0-9]*\.(?!py)(.*)")
    for f in os.listdir(direc):
        if re.match(pat, f) is not None:
            os.remove(os.path.join(direc, f))
            jud = True
    return jud
