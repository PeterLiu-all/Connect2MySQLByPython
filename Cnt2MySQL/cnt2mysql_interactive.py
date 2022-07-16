from platform import python_version, system
from typing import *
from Cnt2MySQL.cnt2mysql_SQLConnector import SQLConnect
from Cnt2MySQL.cnt2mysql_display import into_html_sentence
import Cnt2MySQL.cnt2mysql_TimeKeeper as tkp
from Cnt2MySQL.cnt2mysql_transform import Transformer
import pandas as pd
import re
from sys import executable
from os import popen
import os
from colorama import Fore, Back, Style

VERSION = '1.3.2'     
        
class InteractiveSQLConnect(SQLConnect):
    """
    交互式窗口类，继承自SQLConnect
    Args:
        SQLConnect: 基本SQL连接类
    """
    @tkp.time_keeper.time_monitor
    def __init__(self) -> None:
        """
        初始化交互式窗口对象
        """
        # 调用父级初始化（父级的私有变量无法用正常方法访问）
        super().__init__("", with_file = False)
        # 对输入语句是否结束的分析正则表达式
        self.analyse_pat = re.compile(r"^[\s\S]*;(\n)*")
        # 非安全模式下的各种命令对应的函数
        self.command_sentence_dict = {r"%f": self.exec_file,\
            r"%out": self.output_table, r"%c": self.exec_command,\
                r"%v": self.show_sql_stc, r"%p": self.insert_py}
        # 清屏
        if system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
        # 打印基本信息
        print(f"Cnt2MySQL-Interactive Window-交互式窗口-v{VERSION}".center(65, "-"))
        print(f"interpreter: {executable}".center(70, "-"))
        print(f"version: {python_version()}".center(70, "-"))
        print("Welcome to Peter Liu's interactive Window!".center(70, "-"))
    
    @tkp.time_keeper.time_monitor
    def commit_to_MySQL(self, sql_sentence: str, if_print: bool = True) -> List[pd.DataFrame]:
        """
        重写父级提交语句函数，单句单句提交

        Args:
            sql_sentence (str): 提交语句
            if_print (bool, optional): 是否打印. Defaults to True.

        Returns:
            List[pd.DataFrame]: 返回的表格
        """
        # 无法正常访问父级私有变量，需要改名后才能访问
        assert self._SQLConnect__db is not None
        # 使用cursor()方法创建一个游标对象cursor
        cursor = self._SQLConnect__db.cursor()
        assert cursor is not None
        # 将语句添加入语句集中
        self.sql_list.append(sql_sentence)
        try:
            cursor.execute(sql_sentence)
            self._results.append(cursor.fetchall())
        except:
            print("执行失败！请查看该句是否有语法错误！")
            self._results.append([])
        # 打印结果
        if if_print:
            self.PrtResult(self._results[-1])
        # 关闭游标
        cursor.close()
        # 提交事务
        self._SQLConnect__db.commit()
        
    @tkp.time_keeper.time_monitor
    def analyse_sentence(self, sql_sentence:str)-> bool:
        """
        分析语句是否结束

        Args:
            sql_sentence (str): 语句

        Returns:
            bool: 是否结束
        """ 
        if self.analyse_pat.match(sql_sentence) is None:
            return False
        else:
            return True
        
    @tkp.time_keeper.time_monitor
    def launch_interactive(self, visualize: bool = True, unsafe: bool = False):
        """
        启动交互式窗口

        Args:
            visualize (bool, optional): 是否在所有任务结束后可视化. Defaults to True.
            unsafe (bool, optional): 是否开启非安全模式. Defaults to False.
        """
        # 再次确认是否开启非安全模式
        if unsafe:
            print(Fore.RED + Style.BRIGHT)
            vrf:str = input("警告！你正在使用不安全的模式，可能会造成损失！请问是否继续？(Y|n)")
            print(Style.RESET_ALL)
            if vrf != "Y": 
                print("已退出！")
                return
        # 连接数据库
        try:
            self.Connect2Server()
        except:
            print("连接数据库出错！")
            print("请调用Connect2Server()重试！")
        assert self._SQLConnect__db is not None
        s = "" # 当前语句
        while True:
            # 获取输入
            s: str = input(">>> ")
            # 是否为退出语句
            if s in ["quit", "quit;", "exit", "exit;"]: break
            # 非安全模式
            if unsafe:
                flag = False
                # 检测是哪一个命令
                for k in self.command_sentence_dict.keys():
                    pat = re.compile(f"^{k}:([\s\S]*)")
                    pat_obj = pat.match(s) 
                    if pat_obj is not None:
                        # 获取命令内容
                        ctt:str = pat_obj.group(1)
                        ctt = ctt.strip()
                        # 命令内容不得为空
                        if ctt != "":
                            try:
                                # 获取对应函数并执行
                                self.command_sentence_dict[k](pat_obj.group(1))
                            except:
                                print("\a"+f"出错了！请检查你的{k}命令语句！")
                        else: print(f"{k}:空的内容！")
                        flag = True
                        break
                # 使用了命令不当再提交到MySQL端
                if flag: continue
            # 防止语句未完
            while self.analyse_sentence(s) == False:
                s += input("... ")
            self.commit_to_MySQL(s, True)
        # farewell
        print("bye~~")
        # 可视化
        if visualize: into_html_sentence(self._results, self.sql_list)
        # 显示耗时
        print(tkp.time_keeper.calculate_used_time())
        
    @tkp.time_keeper.time_monitor
    def exec_file(self, fname:str):
        """
        执行sql文件语句或python文件

        Args:
            fname (str): 文件名
        """
        # 判断文件后缀名
        fname = fname.strip()
        splited_path = os.path.splitext(fname)
        # 执行
        if splited_path[-1] == ".py":
            rsp = popen(f"python {fname}")
            for stc in rsp:
                print(stc.strip("\n"))
        elif splited_path[-1] == ".sql":
            with open(fname) as f:
                lines = f.read().split(";")
                for l in lines:
                    l = l.strip("\n")
                    if l == "": continue
                    l += ";"
                    print(">>> "+l)
                    self.commit_to_MySQL(l)
        else: print("未知文件名！")
        
    @tkp.time_keeper.time_monitor
    def output_table(self, opt:str):
        """
        保存为其他格式

        Args:
            opt (str): 选项
        """
        
        opt = opt.strip()
        if opt == "":
            print("recive nothing!")
            return
        opt_set_ori = opt.split(" ")
        # 去除无用项
        opt_set = [item for item in opt_set_ori if item != ""]
        # 防止有少于三个选项
        if len(opt_set) < 2:
            opt_set.append(".")
        elif len(opt_set) < 3:
            opt_set.append("html")
        # 分别解析三个选项
        if opt_set[0] == "all":
            # 全部输出
            trs = Transformer(self.dfSet, direc=opt_set[1])
        else: 
            # 只输出上一句
            trs = Transformer([self.dfSet[-1]], direc=opt_set[1])
        if opt_set[2] in trs.format_dict:
            # 调用相应输出函数
            trs.format_dict[opt_set[2]]()
        else: trs.format_dict['html']()
        
    @tkp.time_keeper.time_monitor    
    def exec_command(self, cmd:str):
        """
        执行shell命令

        Args:
            cmd (str): shell命令
        """
        rsp = popen(cmd) 
        for stc in rsp.readlines():
            print(stc)
            
    @tkp.time_keeper.time_monitor        
    def insert_py(self, py_stc:str):
        """
        执行python语句

        Args:
            py_stc (str): py语句
        """
        exec(py_stc.strip())
        
    @tkp.time_keeper.time_monitor    
    def show_sql_stc(self, visualize: str = "vl"):
        """
        显示所有已经执行的sql语句

        Args:
            visualize (str, optional): 是否可视化. Defaults to "vl".
        """
        visualize = visualize.strip()
        # 是否可视化
        if visualize == "vl":
            self.PrtAllResult(True)
        else:
            self.PrtAllResult(False)
            
if __name__ == "__main__":
    InteractiveSQLConnect.launch_interactive()
        