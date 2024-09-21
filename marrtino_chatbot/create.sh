#!/bin/bash 

# create enviroment
python3 -m venv myenv

# per activate
source $HOME/src/marrtino_chatbot/myenv/bin/activate
pip3 install -r requirements.txt
python3 app2.py


