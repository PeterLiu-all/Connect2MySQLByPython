

Default_CSS:str = '''
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
        transition: 1s;
    }
    h1{
        text-align: center;
        font-size: 2em;
        font-family: 'Lucida Console',楷体, 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        color: bisque;
        transition: 1s;
    }
    td:hover{
        transform: translate(-3px, -4px);
        border-color: rgba(187, 178, 178, 0.575);
		filter: drop-shadow(15px 5px 5px rgba(208, 208, 208, 0.832));
    }
	h1:hover{
        color: rgba(255, 187, 0, 0.848);
        filter: drop-shadow(15px 5px 5px rgba(255, 187, 0, 0.37));
    }
    td:active{
		filter: contrast(2);
	}
        '''

article_with_navi:str = """
body{
    display: inline-flexbox;
    background-image: url(https://cdn.staticaly.com/gh/PeterLiu-all/image-hosting@master/20220708/aedrian-oR8z-NvZkOo-unsplash.mqg625zknmo.webp);
    background-color: black;
    background-size: cover;
    height: fit-content;
    background-position: 20%;
}
div.navi{
    display: inline-flexbox;
    height: fit-content;
    min-height: 820px;
    width: 30%;
    margin: 0;
    background-color: rgba(255, 255, 255, 0.1);
    background-image: none;
    padding: 10px 0;
    box-shadow: 0 8px 16px 0 rgba(151, 144, 144, 0.2);
    float: left;
    border: 0 solid;
}

div.arti{
    min-height: 820px;
    float: right;
    width: 70%;
    background-color: rgba(255, 255, 255, 0.1);
    padding: 10px 0;
    box-shadow: 0 8px 16px 0 rgba(151, 144, 144, 0.2);
    border: 0 solid;
}
div.guide{
    background-color: transparent;
    margin: 0;
    transition: 1s;
}
div.guide:hover{
    background-color: rgba(225, 233, 233, 0.4);
    border-radius: 10px;
    cursor: pointer;
    transform: translate(2px,-2px);
}
p{
    font-family:  'Lucida Console',楷体, Chiller, 'Times New Roman', fantasy;
    font-weight: bold;
    font-size: larger;
}
a{
    font-family:  'Lucida Console',楷体, Chiller, 'Times New Roman', fantasy;
    text-align: left;
    text-decoration: none;
    color: whitesmoke;
}"""
       
def read_css_file(css_file:str)-> str:
    with open(css_file, "r") as f:
        CSS_def = f"<style>\n{f.read}\n<\style>\n"
    return CSS_def