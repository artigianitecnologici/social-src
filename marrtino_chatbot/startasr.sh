#!/bin/bash 
cd  $HOME/src/marrtino_chatbot
source $HOME/src/marrtino_chatbot/myenv/bin/activate
cd websocket-microphone
python3 asr_server_microphone.py


