from Cnt2MySQL import SQLConnect, Transformer
import Cnt2MySQL


# filename是你自己的sql文件名
sql_obj = SQLConnect("test.sql")
# title是你的服务器配置名
sql_obj.readConfig(cfgFile="config.ini.tmp", title="Default")
# 连接了之后自动打印
# 请在config.ini中配置你的MySQL服务器
sql_obj.commit_to_MySQL(sql_obj.sql_list, visualize=False)
sql_obj.PrtAllResult(visualize=True)
# sql_obj.reset()

# 在连接并获取SQL语句执行结果后
Transformer.clean_all()
trf = Transformer(sql_obj.dfSet)
trf.to_html()

print(sql_obj.run_time)
# TimeKeeper.calculate_used_time()

# 上传当前配置
# sql_obj.uploadConfig2MySQL()
# 下载数据库中全部配置
# sql_obj.downloadConfig("config.ini.tmp")
