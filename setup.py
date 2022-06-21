from setuptools import setup

long_description = "Failed to open file!"
with open("README.md", "r") as f:
    long_description = f.read()
setup(
    name="Cnt2MySQL",
    version="1.22",
    author="PeterLiu",
    author_email="peterliuforever@gmail.com",
    description="Easier way to connect to MySQL by Python",
    long_description=long_description,
    license="GPL",
    url="https://github.com/PeterLiu-all/Connect2MySQLByPython",
    data_files=["start.sh", "test.py", "test.sql", "config.ini"],
    packages=["Cnt2MySQL"],
    install_requires=[
        'colorama',
        'matplotlib',
        'pandas',
        'PyMySQL',
        'tabulate'
        ]  
)