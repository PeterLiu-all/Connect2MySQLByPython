# 安装conda
# mkdir anaconda
# cd anaconda
# wget https://repo.anaconda.com/archive/Anaconda3-2018.12-Linux-x86_64.sh
# sudo bash Anaconda3-5.2.0-Linux-x86_64.sh

# conda 创建虚拟环境
# conda create -n cnt2mysql python=3.7
# conda activate cnt2mysql

# 安装依赖
pip install -r requirements.txt
# 打包脚本
pyinstaller -F Cnt2MySQLInteractive.py -n cnt2mysql

# 删除虚拟环境
# conda deactivate
# conda remove -n cnt2mysql

# 将可执行文件转移到可执行路径
sudo mv ./dist/cnt2mysql /usr/local/bin/