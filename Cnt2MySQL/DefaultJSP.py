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