from Cnt2MySQL.cnt2mysql_TimeKeeper import time_keeper
from Cnt2MySQL import InteractiveSQLConnect
import sys
import argparse
from colorama import Fore, Style


@time_keeper.time_monitor
def main():
    # 定义各种选项
    opt_psr = argparse.ArgumentParser(usage=f"python {sys.argv[0]} [OPTIONS]", add_help=False)
    opt_psr.add_argument("-c", "--cfg", action="store", dest="cfgfile", default="config.ini", help="配置文件名",
                         type=str)
    opt_psr.add_argument("-t", "--title", action="store", dest="title", default="Default", help="配置标题", type=str)
    opt_psr.add_argument("-v", "--visualize", action="store_true", dest="if_visualize", help="开启简易可视化")
    opt_psr.add_argument("-f", "--withfile", action="store_true", dest="with_file", help="是否使用配置文件")
    opt_psr.add_argument("-s", "--safe", action="store_true", dest="if_safe", help="开启安全模式")
    opt_psr.add_argument("-ht", "--host", action="store", dest="host", default="127.0.0.1", help="IP地址", type=str)
    opt_psr.add_argument("-prt", "--port", action="store", dest="port", default=3306, help="端口号", type=int)
    opt_psr.add_argument("-pwd", "--passwd", action="store", dest="password", default="123456", help="用户密码",
                         type=str)
    opt_psr.add_argument("-u", "--user", action="store", dest="user", default="root", help="用户名", type=str)
    opt_psr.add_argument("-crt", "--charset", action="store", dest="charset", default="utf8", help="使用的字符集",
                         type=str)
    # 手动定义帮助（添加更多格式）
    opt_psr.add_argument(
        "-h", "--help",
        action='store_true', dest="help",
        help=('show this help message and exit'))
    # 解析参数
    args = opt_psr.parse_args()
    # 是否打印帮助
    inter = InteractiveSQLConnect(opt_psr)
    if args.help:
        inter.Interactive_help()
        sys.exit()
    # 创建交互窗口对象

    # 是否使用配置文件
    if not args.with_file:
        inter.manual_set_config(args.host, args.port, args.user, args.password, args.charset)
    else:
        inter.readConfig(args.cfgfile, args.title)
    # 启动交互式窗口
    inter.launch_interactive(True if args.if_visualize else False, False if args.if_safe else True)


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(err)
        print("出错了！请在命令后加上-h查看帮助！")
