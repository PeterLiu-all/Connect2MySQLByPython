global Default_CSS

Default_CSS:str = '''
<style>
    table{
        width: fit-content;
        height: auto;
        font-size: larger;
        font-family: 'Lucida Console',楷体, 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        font-weight: bold;
        background-color: rgba(255, 255, 255, 1);
        padding: 0;
        margin: auto;
        border-width: 0;
        outline-style: solid;
        outline-color: rgba(2, 2, 2, 0.7);
    }
    tr{
    padding: 0;
    margin: 0;
    border-color: rgba(170, 170, 170, 0.4);
    }
    td{
        padding: 10px;
        margin: 0;
        font-size: large;
        text-align: right;
        border-color: rgba(170, 170, 170, 0.4);
    }
    h1{
        text-align: center;
        font-size: 2em;
        font-family: 'Lucida Console',楷体, 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        color: bisque;
    }
</style>\n
        '''
        
def read_css_file(css_file:str)-> str:
    with open(css_file, "r") as f:
        Default_CSS = f"<style>\n{f.read}\n<\style>\n"
    return Default_CSS