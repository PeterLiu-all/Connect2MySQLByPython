from Cnt2MySQL import SQL,transform

# filename是你自己的sql文件名
sql_obj = SQL.SQL_Connect("test.sql")
# title是你的服务器配置名
sql_obj.readConfig(title="Default")
# 连接了之后自动打印
# 请在config.ini中配置你的MySQL服务器
sql_obj.conn_mysql()

trf = transform.Transformer(sql_obj.dfSet)
trf.to_markdown()
