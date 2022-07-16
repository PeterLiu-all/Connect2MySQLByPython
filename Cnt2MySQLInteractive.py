from Cnt2MySQL import InteractiveSQLConnect
import sys
import argparse
from colorama import Fore, Style

def main():
    # 定义帮助文字
    desc:str = """
简易的MySQL语句执行交互式窗口
支持可视化，在非安全模式下支持执行python语句、shell命令等
    """
    epi:str = """
非安全模式下各种命令使用帮助：
    ！！！注意，以下命令可能具有极大的安全隐患，请慎重决定是否开启非安全模式（默认开启）
        %f:[文件名]支持.py、.sql文件，.py文件可以直接执行（不在当前进程），.sql文件则在当前进程中直接执行其语句，示例：%f: test.py | %f: test.sql
        %out:[all|last 导出路径 文件格式（不带.）]将执行过的命令导出为各种格式（transform模块支持的格式），包括pdf,html,markdown,image等，示例：%out: all . html
        %c:[shell命令]执行shell命令，示例：%c: clear
        %v:[vl|nvl]显示已执行的语句，vl表示可视化显示，nvl表示仅打印，示例：%v: vl
        %p:[python语句]在当前进程中执行python语句，示例：%p: print('Hello Cnt2MySQL!')
    """
    # 定义各种选项
    opt_psr = argparse.ArgumentParser(usage=f"python {sys.argv[0]} [OPTIONS]", add_help=False)
    opt_psr.add_argument("-c", "--cfg", action="store", dest="cfgfile", default="config.ini", help="配置文件名", type=str)
    opt_psr.add_argument("-t", "--title", action="store", dest="title", default="Default", help="配置标题", type=str)
    opt_psr.add_argument("-v", "--visualize", action="store_true", dest="if_visualize", help="开启简易可视化")
    opt_psr.add_argument("-f", "--withfile", action="store_true", dest="with_file", help="是否使用配置文件")
    opt_psr.add_argument("-s", "--safe", action="store_true", dest="if_safe", help="开启安全模式")
    opt_psr.add_argument("-ht", "--host", action="store", dest="host", default="127.0.0.1", help="IP地址", type=str)
    opt_psr.add_argument("-prt", "--port", action="store", dest="port", default=3306, help="端口号", type=int)
    opt_psr.add_argument("-pwd", "--passwd", action="store", dest="password", default="123456", help="用户密码", type=str)
    opt_psr.add_argument("-u", "--user", action="store", dest="user", default="root", help="用户名", type=str)
    opt_psr.add_argument("-crt", "--charset", action="store", dest="charset", default="utf8", help="使用的字符集", type=str)
    # 手动定义帮助（添加更多格式）
    opt_psr.add_argument(
        "-h", "--help",
        action='store_true', dest= "help",
        help=('show this help message and exit'))
    # 解析参数
    args = opt_psr.parse_args()
    # 是否打印帮助
    if args.help:
        # 以不同颜色与格式打印帮助
        print(Fore.MAGENTA + Style.BRIGHT)
        print(desc)
        print(Fore.BLUE + Style.BRIGHT)
        opt_psr.print_help()
        print(Style.RESET_ALL)
        print(Fore.RED + Style.BRIGHT)
        print(epi)
        print(Style.RESET_ALL)
        sys.exit()
    # 创建交互窗口对象
    inter = InteractiveSQLConnect()
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