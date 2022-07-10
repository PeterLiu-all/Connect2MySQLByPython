import re
from configparser import ConfigParser
from time import time
from typing import List, Sequence, Tuple, Union, Optional

import pandas as pd
import pymysql
from colorama import Fore, Back, Style
import asyncio
from Cnt2MySQL.cnt2mysql_display import into_html_sentence


class SQL_Connect:
    def __init__(self, filename: str = "test.sql", config: str = "config.ini") -> None:
        """初始化

        Args:
            filename (str, optional): SQL文件名. Defaults to "test.sql".
            config (str, optional): 配置文件名. Defaults to "config.ini".
        """
        self.start_time = time()
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
            print(f"或许您当前目录没有{filename}?")
            print('''
                    with open([filename], "r") as f:
                        self._to_send = "".join(f.readlines())
                    self.sql_list = []
                    self.toSqlList()
                  ''')
            print("提交语句自动初始化为SHOW DATABASES;")
            self._to_send = "SHOW DATABASES;"
        self.sql_list: List[str] = []
        self.toSqlList()
        self.cursor = None
        # 正则表达式，消除语句中的注释
        self.__comment_pat: re.Pattern = re.compile(r"(^(\n)*--(.*))|(^\n$)")
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
            服务器配置信息：（为安全起见，将不会显示密码）
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
        except:
            print("未找到配置文件！")
            print("初始配置将自动设置为：")
            print(self)
            return
        try:
            cfg_list = cfg[title]
            self.__host, self.__port, self.__user, self.__passwd, self.__charset = cfg_list["host"], int(
                cfg_list["port"]), cfg_list["user"], cfg_list["passwd"], cfg_list["charset"]
        except:
            print("配置失败！")
            print("初始配置将自动设置为：")
            print(self)
            return

    def changeConfig(self, cfgFile: str = "config.ini", title: str = "Default") -> None:
        """改变配置信息

        Args:
            cfgFile (str, optional): 配置文件名 Defaults to "config.ini".
            title (str, optional): 子配置名 Defaults to "Default".
        """
        self.cfgFile = cfgFile
        cfg: ConfigParser = ConfigParser()
        try:
            cfg.read(self.cfgFile)
        except:
            print("未找到配置文件！")
            print("目前配置为：")
            print(self)
            return
        try:
            for option in self.__options:
                new: str = input(f"请输入[{title}]的{option}属性值:")
                cfg.set(title, "host", new if new is not None else cfg[title][option])
        except:
            print("配置失败！")
            print("当前配置为：")
            print(self)
            return

    def changeServer(self):
        self.__host = input("请输入服务器地址：")
        tmp_port: str = input("请输入端口号：")
        while not tmp_port.isdigit():
            tmp_port = input("端口号必须为数字！请再次输入端口号：")
        self.__port = int(tmp_port)
        self.__user = input("请输入用户名：")
        self.__passwd = input("请输入用户密码：")
        tmp_passwd: str = input("请输入字符编码：(默认utf8请回车)")
        self.__passwd = "utf8" if tmp_passwd == "" else tmp_passwd
        self.Connect2Server()

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
            print("请检查您的配置！")
            print("您当前的配置为:")
            print(self)

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
    def PrtAllResult(self, visualize: bool = True) -> None:
        """
        一次性打印所有结果

        Args:
            visualize (bool, optional): 是否可视化. Defaults to True.
        """
        if len(self._results) != len(self.sql_list):
            print("查询语句与查询结果长度不匹配！请检查您的代码！")
            return
        for query, res in zip(self._results, self.sql_list):
            print(Fore.BLUE + Style.DIM)
            print(query)
            print(Style.RESET_ALL)
            print(res)
        if visualize:
            into_html_sentence(self._results, self.sql_list)

    def reset(self) -> None:
        """重置所有输入输出（不含配置）
        """
        self._results.clear()
        self.dfSet.clear()
        self.collabel.clear()
        self._to_send = ""
        self.sql_list.clear()
        
    @property
    def used_time(self) -> str:
        return f"used time: {time() - self.start_time}s"

    def uploadConfig2MySQL(self, title: str = "Default") -> List[pd.DataFrame]:
        # 如果当前用户没有权限，则使用GRANT ALL PRIVILEGES ON *.* TO `{username}`@`localhost`;
        # username是当前用户名
        port = str(self.__port)
        to_update = [
            "CREATE DATABASE IF NOT EXISTS `Cnt2MySQL_Config`;",
            "USE `Cnt2MySQL_Config`;",
            f"DROP TABLE IF EXISTS `Config_{title}`  ",
            f'''
            CREATE TABLE `Config_{title}`  (
                `id` int(10) NOT NULL AUTO_INCREMENT,
                `options` varchar(50) NOT NULL DEFAULT '',
                `value` varchar(50) NOT NULL DEFAULT '',
                PRIMARY KEY (`id`)
            ) ENGINE=INNODB DEFAULT CHARSET = utf8;
            ''',
            f'''
            INSERT INTO `Config_{title}` ( `options`, `value` )
                       VALUES
                       ("host", "{self.__host}"),
                       ("port", "{port}"),
                       ("user", "{self.__user}"),
                       ("password", "{self.__passwd}"),
                       ("charset", "{self.__charset}");
            '''
        ]
        return self.commit_to_MySQL(to_update)

    def downloadConfig(self, file_name: str = "config.ini") -> None:
        to_download = [
            "USE `Cnt2MySQL_Config`;",
            "SHOW TABLES;"
        ]
        with open(file_name, "w") as f:
            for chart in self.commit_to_MySQL(to_download)[-1].to_numpy():
                chart_name: str = chart[0]
                tmp_set = self.commit_to_MySQL([
                    "USE `Cnt2MySQL_Config`;",
                    f"SELECT `options`, `value` FROM {chart_name}"
                ])[-1].to_numpy()
                title = chart_name.split("_")[-1]
                f.write(f"[{title}]\n")
                for i in range(len(tmp_set)):
                    f.write(f"{self.__options[i]}:{tmp_set[i][0]}\n")
                f.write("\n")

    def commit_to_MySQL(self, sql_list: List[str], if_print: bool = True,\
            clear_dfSet:bool = True, visualize: bool = True) -> List[pd.DataFrame]:
        """连接数据库并获取结果

        Returns:
            List[pd.DataFrame]: 所有结果的DataFrame表示的列表
        Args:
            sql_list (List[str]): 要执行的语句
            if_print (bool, optional): 是否打印结果. Defaults to True.
            clear_dfSet (bool, optional): 是否在执行本次任务前清除之前的数据. Defaults to True.
            visualize (bool, optional): 是否可视化. Defaults to True.
        """

        try:
            self.Connect2Server()
        except:
            print("连接数据库出错！")
            print("请调用self.Connect2Server()重试！")
        assert self.__db is not None
        # 使用cursor()方法创建一个游标对象cursor
        cursor = self.__db.cursor()
        if clear_dfSet:
            self.dfSet.clear()
        # 拆分成多个单句，一句一句执行
        self.sql_list = sql_list
        for idx in self.sql_list:
            if idx is not None:
                if len(idx) >= 2 and re.match(self.__comment_pat, idx) is not None:
                    continue
                if if_print:
                    print(Fore.GREEN + Style.DIM)
                    print("sql_sentence:" + idx)
                    print(Style.RESET_ALL)
                # 执行SQL
                try:
                    cursor.execute(idx)
                except:
                    print("执行失败！请查看该句是否有语法错误！")
                    continue
                self._results.append(cursor.fetchall())
                if if_print:
                    self.PrtResult(self._results[-1])
        if visualize:
            into_html_sentence(self._results, self.sql_list)
        # 关闭游标
        cursor.close()
        # 提交事务
        self.__db.commit()
        # 关闭连接
        self.__db.close()
        return self.dfSet

    async def __conn_mysql_async_inner(self, sentence: str, if_print: bool = True):
        assert self.cursor is not None
        self.dfSet.clear()
        if sentence is not None:
            if len(sentence) >= 2 and re.match(self.__comment_pat, sentence) is not None:
                return
            if if_print:
                print(Fore.GREEN + Style.DIM)
                print("sql_sentence:" + sentence)
                print(Style.RESET_ALL)
            # 执行SQL
            self.cursor.execute(sentence)
            self._results.append(self.cursor.fetchall())
            if if_print:
                self.PrtResult(self._results[-1])
        return self.cursor

    async def conn_mysql_async(self, sql_list: List[str], if_print: bool = True) -> List[pd.DataFrame]:
        try:
            self.Connect2Server()
        except:
            print("连接数据库出错！")
            print("请调用self.Connect2Server()重试！")
        assert self.__db is not None
        # 使用cursor()方法创建一个游标对象cursor
        self.cursor = self.__db.cursor()
        tasks = [asyncio.create_task(self.__conn_mysql_async_inner(
            sentence, if_print)) for sentence in sql_list]
        # await asyncio.gather(tasks)
        for task in tasks:
            await task
        into_html_sentence(self._results, sql_list)
        assert self.cursor is not None
        # 关闭游标
        self.cursor.close()
        # 提交事务
        self.__db.commit()
        # 关闭连接
        self.__db.close()
        return self.dfSet
