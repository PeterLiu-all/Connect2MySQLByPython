import re
from configparser import ConfigParser
from typing import List, Sequence, Tuple, Union, Optional

import pandas as pd
import pymysql
from colorama import Fore, Back, Style


class SQL_Connect:
    def __init__(self, filename: str = "test.sql", config: str = "config.ini") -> None:
        """初始化

        Args:
            filename (str, optional): SQL文件名. Defaults to "test.sql".
            config (str, optional): 配置文件名. Defaults to "config.ini".
        """
        self.__db: Optional[pymysql.Connection] = None
        self.dfSet: List[pd.DataFrame] = []
        self.collabel: List[Union[str, int]] = []
        self._results: List[Sequence] = []
        # 服务器信息
        self.__host: str = "localhost"
        self.__port: int = 3306
        self.__user: str = "root"
        self.__passwd: str = "123456"
        self.__charset: str = "utf8"
        self.cfgFile: str = config
        self.__options: Tuple = ("host", "port", "user", "passwd", "charset")
        self._to_send: str = ""
        # 读取SQL文件
        try:
            with open(filename, "r") as f:
                self._to_send = "".join(f.readlines())
        except:
            print("打开sql文件出错！请按如下步骤重试")
            print('''
                    with open([filename], "r") as f:
                        self._to_send = "".join(f.readlines())
                    self.sql_list = []
                    self.toSqlList()
                  ''')
        self.sql_list: List[str] = []
        self.toSqlList()
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
        self.__attrs: Tuple = (
            "__db", "dfSet", "collabel", "_results",
            "__host", "__port", "__user", "__passwd", "__charset", "cfgFile",
            "__options", "_to_send", "sql_list"
        )
        self.__real_attrs: Tuple = (
            "dfSet", "collabel", "_results", "cfgFile", "_to_send", "sql_list"
        )

    def __str__(self) -> str:
        """__str__
        返回服务器配置信息
        """
        return(f'''
            Host:{self.__host}
                Port:{self.__port}
                User:{self.__user}
                Password:******
                CharSet:{self.__charset}
              ''')

    def __add__(self, apd: "SQL_Connect") -> "SQL_Connect":
        """__add__
        将两个SQL_Connect对象内的数据相加
        """
        self._results += apd._results
        self.dfSet += apd.dfSet
        self.collabel += apd.collabel
        self._to_send += apd._to_send
        self.sql_list += apd.sql_list
        return self

    def __len__(self) -> int:
        """
        返回SQL语句列表长度

        Returns:
            int
        """
        return len(self.sql_list)

    def __getitem__(self, key: str) -> Optional[Union[str, int, List, pymysql.Connection, pd.DataFrame]]:
        """
        通过方括号获取属性

        Args:
            key (str): 属性名

        Returns:
            Optional[Union[str, int, List, pymysql.Connection, pd.DataFrame]]: 返回属性
        """
        if key not in self.__real_attrs:
            print(f"没有{key}这个属性！")
            return None
        else:
            return getattr(self, key)

    def readConfig(self, cfgFile: str = "config.ini", title: str = "Default") -> None:
        """读取配置文件

        Args:
            cfgFile (str, optional): 配置文件名 Defaults to "config.ini".
            title (str, optional): 子配置名 Defaults to "Default".
        """
        self.cfgFile = cfgFile
        cfg: ConfigParser = ConfigParser()
        try:
            cfg.read(self.cfgFile)
        except FileNotFoundError:
            print("未找到配置文件！")
        cfg_list = cfg[title]
        self.__host = cfg_list["host"]
        self.__port = int(cfg_list["port"])
        self.__user = cfg_list["user"]
        self.__passwd = cfg_list["passwd"]
        self.__charset = cfg_list["charset"]

    def changeConfig(self, cfgFile: str = "config.ini", title: str = "Default") -> None:
        """改变配置信息

        Args:
            cfgFile (str, optional): 配置文件名 Defaults to "config.ini".
            title (str, optional): 子配置名 Defaults to "Default".
        """
        self.cfgFile = cfgFile
        cfg: ConfigParser = ConfigParser()
        cfg.read(self.cfgFile)
        for option in self.__options:
            new: str = input(f"请输入[{title}]的{option}属性值:")
            cfg.set(title, "host",
                    new if new is not None else cfg[title][option])

    def Connect2Server(self) -> None:
        """数据库连接
        """
        try:
            self.__db = pymysql.Connect(
                host=self.__host,
                port=self.__port,
                user=self.__user,
                passwd=self.__passwd,
                charset=self.__charset
            )
        except:
            print("无法连接服务器！")

    def toSqlList(self) -> None:
        """将sql语句转换为以;为分隔的列表
        """
        # 解析传进来的SQL脚本,sql脚本已';'结束
        self.sql_list = self._to_send.split(';')
        # 删除最后一个空字符串
        self.sql_list.pop()

    def PrtResult(self, result: Sequence[Sequence]) -> None:
        """PrtResult
        对单条结果进行pandas的DataFrame转换并打印
        """
        if result.__len__() > 0:
            print(Fore.BLUE + Style.DIM)
            print(result)
            print(Style.RESET_ALL)
            colname: List[Union[str, int]] = ['index']
            for i in range(1, len(result[0])):
                colname.append(i)
            self.collabel = colname
            df = pd.DataFrame(result, columns=colname)
            if len(colname) > 1:
                df.set_index(['index'], inplace=True)
            self.dfSet.append(df)
            print(df)

    def PrtAllResult(self) -> None:
        """PrtAllResult
        一次性打印所有结果
        """
        for query, res in zip(self._results, self.dfSet):
            print(Fore.BLUE + Style.DIM)
            print(query)
            print(Style.RESET_ALL)
            print(res)

    def reset(self) -> None:
        """重置所有输入输出（不含配置）
        """
        self._results.clear()
        self.dfSet.clear()
        self.collabel.clear()
        self._to_send = ""
        self.sql_list.clear()

    def conn_mysql(self) -> List[pd.DataFrame]:
        """连接数据库并获取结果

        Returns:
            List[pd.DataFrame]: 所有结果的DataFrame表示的列表
        """
        try:
            self.Connect2Server()
        except:
            print("连接数据库出错！")
            print("请调用self.Connect2Server()重试！")
        assert self.__db is not None
        # 使用cursor()方法创建一个游标对象cursor
        cursor = self.__db.cursor()
        # 正则表达式，消除语句中的注释
        pat: re.Pattern = re.compile(r"(^(\n)*--(.*))|(^\n$)")
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
                self._results.append(cursor.fetchall())
                self.PrtResult(self._results[-1])
        # 关闭游标
        cursor.close()
        # 提交事务
        self.__db.commit()
        # 关闭连接
        self.__db.close()
        return self.dfSet
