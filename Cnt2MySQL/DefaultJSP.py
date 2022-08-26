"""
本文件定义了查询结果网页的基本jsp脚本
"""

# 实时时间函数
change_date = """
function changeDate(jud, title){
    if(jud == true){
        let d = new Date()
        let now = d.toLocaleDateString(undefined, options);
        document.getElementById("date").innerText = now;
        if(title) movingTittle(d.getSeconds())
    }
}
const options = {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "numeric",
        minute: "numeric",
        second: "numeric",
      };
window.setInterval("changeDate(true, false);", 1000);"""
