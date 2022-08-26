from typing import Callable, Dict, List
import pandas
import os
import re
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from Cnt2MySQL.DefaultCSS import Default_CSS
import Cnt2MySQL.cnt2mysql_TimeKeeper as tkp


class Transformer:
    @tkp.time_keeper.time_monitor
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
        self.format_dict = {"html": self.to_html, "csv": self.to_csv,
                            "img": self.to_img, "pdf": self.to_pdf, "txt": self.to_txt,
                            "md": self.to_markdown, "excel": self.to_excel,
                            "all": self.to_all}

    @staticmethod
    @tkp.time_keeper.time_monitor
    def clean_all(name: str = "transform", direc: str = ".") -> bool:
        jud: bool = False
        pat: re.Pattern = re.compile(name + r"[0-9]*\.(?!py)(.*)")
        for f in os.listdir(direc):
            if re.match(pat, f) is not None:
                os.remove(os.path.join(direc, f))
                jud = True
        return jud

    @tkp.time_keeper.time_monitor
    def __NormalModule(self, func: Callable, ext: str) -> None:
        """模板

        Args:
            func (Callable): 使用的函数
            ext (str): 后缀名
        """
        for i in range(len(self.dataframes)):
            df = self.dataframes[i]
            func(df, f"{self.pname}{i + 1}" + ext)

    @tkp.time_keeper.time_monitor
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

    @tkp.time_keeper.time_monitor
    def to_img(self) -> None:
        for i in range(len(self.dataframes)):
            df = self.dataframes[i]
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.axis('tight')
            ax.axis('off')
            the_table = ax.table(cellText=df.values,
                                 colLabels=df.columns, loc='center')
            plt.savefig(f"{self.pname}{i}.png")

    @tkp.time_keeper.time_monitor
    def to_markdown(self) -> None:
        self.__NormalModule(pandas.DataFrame.to_markdown, ".md")

    @tkp.time_keeper.time_monitor
    def to_html(self) -> None:
        def default_to_html(df: pandas.DataFrame, name: str):
            df.to_html(name)
            # 设置CSS样式
            with open(name, "r", encoding="UTF-8") as f:
                file_content = f"<style>\n{Default_CSS}</style>\n" + f.read()
            with open(name, "w", encoding="UTF-8") as f:
                f.write(f"{file_content}\n\n")

        self.__NormalModule(default_to_html, ".html")

    @tkp.time_keeper.time_monitor
    def to_csv(self) -> None:
        self.__NormalModule(pandas.DataFrame.to_csv, ".csv")

    @tkp.time_keeper.time_monitor
    def to_excel(self) -> None:
        self.__NormalModule(pandas.DataFrame.to_excel, ".xlsx")

    @tkp.time_keeper.time_monitor
    def to_txt(self) -> None:
        def write_to_txt(df: pandas.DataFrame, name: str):
            df_str: Dict = df.to_string()
            with open(name, "w", encoding="UTF-8") as f:
                f.write(f"{df_str}\n\n")

        self.__NormalModule(write_to_txt, ".txt")

    @tkp.time_keeper.time_monitor
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
