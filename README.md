# Connect2MySQLByPython

通过python连接MySQL，使用pymysql

使用config.ini进行配置

使用Pandas一句一句地打印MySQL表格
可以通过Pandas的内置方法将表格导出为Excel，markdown等多种格式

## 获取方式

```bash
git clone https://github.com/PeterLiu-all/Connect2MySQLByPython.git
```

## 使用方法

```python
import SQL
# filename是你自己的sql文件名
sql_obj = SQL.SQL_Connect(filename)
# title是你的服务器配置名
sql_obj.readConfig(title="Default")
# 连接了之后自动打印
# 请在config.ini中配置你的MySQL服务器
sql_obj.conn_mysql()
```

你也可以直接使用文件夹中的test.py进行测试

## 将输出结果导出为其他格式

本项目的transform.py提供了将表格导出为markdown、PDF、png、HTML、csv、excel的方法（多数为pandas的自带方法）

### 使用方法

```python
# 在连接并获取SQL语句执行结果后
trf = transform.Transformer(sql_obj.dfSet)
trf.to_markdown()
```

也可以直接在test.py测试