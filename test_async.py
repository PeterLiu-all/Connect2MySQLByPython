from Cnt2MySQL import SQL_Connect, Transformer
import asyncio
import time

# 测试有ascync和没有async的效率差距
# 我的电脑上大概差0.3~0.5s

# 初始化对象（不计入时间）
sql_obj = SQL_Connect("test.sql")
sql_obj.readConfig(title="Default")
sql_list = sql_obj.sql_list*100
# 无async
start1:float = time.time()
sql_obj.conn_mysql(sql_list)
end1:float = time.time() - start1
# 有async
start2:float = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(sql_obj.conn_mysql_async(sql_list))
end2:float = time.time() - start2
# 打印时间
print(f"NO ASYNC:{end1}")
print(f"WITH ASYNC:{end2}")

