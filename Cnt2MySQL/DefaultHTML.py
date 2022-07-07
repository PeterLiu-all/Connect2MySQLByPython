from Cnt2MySQL.DefaultCSS import Default_CSS, article_with_navi
from Cnt2MySQL.DefaultJSP import change_date

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
  
DefaultFrame_tail:str = """
</body>
</html>"""

arti_head:str = """
<div class="arti">
    <h1 style=\"color: whitesmoke;\">MySQL Results</h1>
    &emsp;&emsp;
    <p id=\"date\" style=\"text-align: center;color: whitesmoke;\">Loading...</p>
    <hr>
    <div style="padding: 20px;">"""
    
arti_tail:str = """
</div>
</div>"""

navi_head:str = """
    <div class="navi">
    <hr>
    <h1 style=\"color: whitesmoke;\">index</h1>
      <hr>"""

navi_tail:str = """
</div>"""

navi_item = [
"""
<div class=\"guide\">
        <a href=\"#""",
"""\"><p class=\"navi\">""",
"""</p></a>
      </div>
      <hr />"""
]