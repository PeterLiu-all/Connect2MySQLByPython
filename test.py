from Cnt2MySQL import SQL_Connect, Transformer


# filename是你自己的sql文件名
sql_obj = SQL_Connect("test.sql")
# title是你的服务器配置名
sql_obj.readConfig(title="Default")
# 连接了之后自动打印
# 请在config.ini中配置你的MySQL服务器
sql_obj.conn_mysql(sql_obj.sql_list)

trf = Transformer(sql_obj.dfSet)
trf.to_html()

# sql_obj.uploadConfig2MySQL()
# sql_obj.downloadConfig("config.ini.tmp")