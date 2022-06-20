#!/bin/sh

# echo -e "trying to install requirements...\n"
# pip install -r requirements.txt
# if [ $? != 0 ]
# then
#     echo -e "\nERROR found in install requirements!\n"
# fi
echo -e "trying to run setup.py...\n"
python3 setup.py build && python3 setup.py install
if [ $? != 0 ]
then
    echo -e "\nERROR found in setup!\n"
    exit -1  
fi
echo -e "running test.py...\n"
python3 test.py 


if [ $? == 0 ]
then
    echo -e "\nif there's Bug, please send e-mail to peterliuforever@gmail.com\n"
else
    echo -e "\nERROR found in test!\n"
fi
