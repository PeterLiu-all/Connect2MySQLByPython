from Cnt2MySQL.DefaultCSS import Default_CSS, article_with_navi
from Cnt2MySQL.DefaultJSP import change_date

"""
本文件定义了查询结果网页的基本HTML框架
"""

#框架头部
DefaultFrame_head = f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SQL_results</title>
    <style>
    {Default_CSS}
    {article_with_navi}
    </style>
    <script>
    {change_date}  
    </script>
  </head>
  <body>"""

# 框架尾部
DefaultFrame_tail:str = """
</body>
</html>"""

# 双栏中正文头部
arti_head:str = """
<div class="arti">
    <h1 style=\"color: whitesmoke;\">MySQL Results</h1>
    &emsp;&emsp;
    <p id=\"date\" style=\"text-align: center;color: whitesmoke;\">Loading...</p>
    <hr>
    <div style="padding: 20px;">"""

# 双栏中正文尾部
arti_tail:str = """
</div>
</div>"""

# 双栏中导航栏头部
navi_head:str = """
    <div class="navi">
    <hr>
    <h1 style=\"color: whitesmoke;\">index</h1>
      <hr>"""
      
# 双栏中导航栏头部
navi_tail:str = """
</div>"""

# 每一个书签的框架
navi_item = [
"""
<div class=\"guide\">
        <a href=\"#""",# 后面跟书签的id
"""\"><p class=\"navi\">""",# 后面跟书签的标题
"""</p></a>
      </div>
      <hr />"""
]