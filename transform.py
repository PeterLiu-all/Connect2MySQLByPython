import pandas
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


class Transformer:
    def __init__(self, dataframes: list[pandas.DataFrame], name: str = "transform") -> None:
        self.dataframes = dataframes
        self.name = name

    def to_markdown(self):
        for i in range(len(self.dataframes)):
            df = self.dataframes[i]
            df.to_markdown(f"{self.name}{i}.md")

    def to_pdf(self):
        for i in range(len(self.dataframes)):
            df = self.dataframes[i]
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.axis('tight')
            ax.axis('off')
            the_table = ax.table(cellText=df.values,
                                 colLabels=df.columns, loc='center')
            pp = PdfPages(f"{self.name}{i}.pdf")
            pp.savefig(fig, bbox_inches='tight')
            pp.close()

    def to_img(self):
        for i in range(len(self.dataframes)):
            df = self.dataframes[i]
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.axis('tight')
            ax.axis('off')
            the_table = ax.table(cellText=df.values,
                                 colLabels=df.columns, loc='center')
            plt.savefig(f"{self.name}{i}.png")

    def to_html(self):
        for i in range(len(self.dataframes)):
            df = self.dataframes[i]
            df.to_html(f"{self.name}{i}.html")

    def to_csv(self):
        for i in range(len(self.dataframes)):
            df = self.dataframes[i]
            df.to_csv(f"{self.name}{i}.csv")

    def to_excel(self):
        for i in range(len(self.dataframes)):
            df = self.dataframes[i]
            df.to_excel(f"{self.name}{i}.xlsx")

    def to_all(self):
        self.to_csv()
        self.to_excel()
        self.to_html()
        self.to_img()
        self.to_markdown()
        self.to_pdf()
