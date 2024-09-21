# marrtino_chatbot

sudo apt install python3.8-venv
sudo apt install python3-pip

# per creare enviroment
python3 -m venv myenv

# per attivarlo
source myenv/bin/activate
pip3 --version
@ installazione librerie
pip3 install -r requirements.txt


# Vosk 

pip3 install vosk
python3 -m pip install sounddevice
pip3 install websockets

# for testing
http://x.x.x.x:5000/

http://x.x.x.x:5000/query-example?query=ciao


http://127.0.0.1:5000/bot?query=ciao

# open firewall
sudo ufw allow 5000

# prerequisiti per lo speech
sudo apt install sox
sudo apt-get install libsox-fmt-all
sudo apt-get install portaudio19-dev

