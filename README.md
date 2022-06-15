# Connect2MySQLByPython
通过python连接MySQL，使用pymysql

使用config.ini进行配置

使用Pandas一句一句地打印MySQL表格
可以通过Pandas的内置方法将表格导出为Excel，markdown等多种格式

## 使用方法
```python
# filename是你自己的sql文件名
sql_obj = SQL.SQL_Connect(filename)
# title是你的服务器配置名
sql_obj.readConfig(title="Default")
# 连接了之后自动打印
# 请在config.ini中配置你的MySQL服务器
sql_obj.conn_mysql()
```