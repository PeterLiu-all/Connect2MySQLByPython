import pymysql
import pandas as pd
import re
from configparser import ConfigParser
from colorama import Fore, Back, Style


class SQL_Connect:
    def __init__(self, filename: str = "test.sql") -> None:
        self.db = pymysql.NULL
        self.dfSet = []
        self.collabel = []
        self.results = []
        self.host = "localhost"
        self.port = 3306
        self.user = "root"
        self.passwd = "123456"
        self.charset = "utf8"
        self.cfgFile = "config.ini"
        self.options = ("host", "port", "user", "passwd", "charset")
        try:
            with open(filename, "r") as f:
                self.to_send = "".join(f.readlines())
        except:
            print("打开sql文件出错！请按如下步骤重试")
            print('''
                    with open([filename], "r") as f:
                        self.to_send = "".join(f.readlines())
                    self.sql_list = []
                    self.toSqlList()
                  ''')
        self.sql_list = []
        self.toSqlList()

    def readConfig(self, cfgFile: str = "config.ini", title: str = "Default"):
        self.cfgFile = cfgFile
        cfg = ConfigParser()
        cfg.read(self.cfgFile)
        cfg_list = cfg[title]
        self.host = cfg_list["host"]
        self.port = int(cfg_list["port"])
        self.user = cfg_list["user"]
        self.passwd = cfg_list["passwd"]
        self.charset = cfg_list["charset"]

    def changeConfig(self, cfgFile: str = "config.ini", title: str = "Default"):
        self.cfgFile = cfgFile
        cfg = ConfigParser()
        cfg.read(self.cfgFile)
        for option in self.options:
            new = input(f"请输入[{title}]的{option}属性值:")
            cfg.set(title, "host",
                    new if new is not None else cfg[title][option])

    def Connect2Server(self):
        # 数据库连接
        self.db = pymysql.Connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            charset=self.charset
        )

    def toSqlList(self):
        # 解析传进来的SQL脚本,sql脚本已';'结束
        self.sql_list = self.to_send.split(';')
        # 删除最后一个空字符创
        self.sql_list.pop()

    def PrtResult(self, result):
        if result.__len__() > 0:
            print(Fore.BLUE + Style.DIM)
            print(result)
            print(Style.RESET_ALL)
            colname = ['index']
            for i in range(1, len(result[0])):
                colname.append(i)
            self.collabel.append(colname)
            df = pd.DataFrame(result, columns=colname)
            if len(colname) > 1:
                df.set_index(['index'], inplace=True)
            self.dfSet.append(df)
            print(df)

    def PrtAllResult(self):
        self.dfSet.clear()
        for res in self.results:
            self.PrtResult(res)

    def reset(self):
        self.results.clear()
        self.to_send = ""
        self.sql_list.clear()

    def conn_mysql(self):
        try:
            self.Connect2Server()
        except:
            print("连接数据库出错！")
            print("请调用self.Connect2Server()重试！")
        # 使用cursor()方法创建一个游标对象cursor
        cursor = self.db.cursor()
        # 正则表达式，消除语句中的注释
        pat = re.compile(r"(^(\n)*--(.*))|(^\n$)")
        self.dfSet.clear()
        # 拆分成多个单句，一句一句执行
        for idx in self.sql_list:
            if idx is not None:
                if len(idx) >= 2 and re.match(pat, idx) is not None:
                    continue
                print(Fore.GREEN + Style.DIM)
                print("sql_sentence:" + idx)
                print(Style.RESET_ALL)
                # 执行SQL
                cursor.execute(idx)
                self.results.append(cursor.fetchall())
                self.PrtResult(self.results[-1])
        # 关闭游标
        cursor.close()
        # 提交事务
        self.db.commit()
        # 关闭连接
        self.db.close()
        return self.dfSet
