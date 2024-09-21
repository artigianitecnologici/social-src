#!/usr/bin/python3
import os,aiml
from flask import Flask,render_template, request, jsonify
import json
from threading import Thread
import sys
import openai

from datetime import datetime

# Create the kernel and learn AIML files
kernel = aiml.Kernel()
#kernel.learn("std-startup.xml")
kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
kernel.verbose(True)
PATH = "/home/src/marrtino_chatbot/"
LOG_PATH = os.path.join(PATH,"log")
# Max numero token di risposta
MAXTOKEN = 100
with open("secrets.json") as f:
    secrets = json.load(f)
    api_key = secrets["api_key"]

openai.api_key = api_key
# keyword per comandi
keyword = "martina"

def left(s, n):
    return s[:n]


def run_code(code):
    global status
    if (code is None):
        return

def log_to_file(question,aiml_answer,chatgpt_answer):
    now = datetime.now()
    data_ora = now.strftime("%d/%m/%Y %H:%M:%S")
    log_file = open("log/log.txt", "a")
    report = data_ora + "\n" +\
        "[QUESTION]:   " + question + ";" +\
        "[AIML]:       " + aiml_answer + ";"  +\
        "[CHATGPT]: " + chatgpt_answer 
       
    log_file.write(report + "\n")
    log_file.close
    # scrive sul file per la successiva importazione
    if (chatgpt_answer != ""):
        bot_file = open("log/user.txt","a")
        bot_file.write("user: " + question+"\n")
        bot_file.write("bot: " + chatgpt_answer+"\n")
        bot_file.close()

def activity(msg):
    #
    return 

def split_string(msg):
    amsg = msg.split('.')
    
    if len(amsg) >= 2:
       result = amsg[0] + ' ' + amsg[1]
    else:
       result = amsg[0]
 
    return result 



# Verifica se è un comando
# ------------------------
def filter(msg):

    msg = msg.lower()
    msglenght = len(msg)
    keylenght = len(keyword)
    if (left(msg,keylenght) == keyword):
        #msgout = command(msg[len(keyword)])
        mycmd =  msg[keylenght+1:msglenght]
        #command(mycmd)
        msgout = "comando: "  + mycmd
       
    else:
        msgout = kernel.respond(msg)
    return msgout


def get_response(messages:list):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=messages,
        max_tokens= MAXTOKEN,
        temperature = 1.0 # 0.0 - 2.0
       
    )
   
   
    return response.choices[0].message

# create the Flask app
app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    myquery  = request.args.get('msg')
    msgaiml = filter(myquery)
    msgout = msgaiml
    if msgaiml == "":
        # if key doesn't exist, returns None
        messages = [
            {"role": "system", "content": "Sei un assistente virtuale chiamata MARRtina e parli italiano."}
        ]
        

        messages.append({"role": "user", "content": myquery})
        new_message = get_response(messages=messages)
        messages.append(new_message)
        msgout = new_message['content']
        msgout = split_string(msgout)

    log_to_file(myquery,msgaiml,msgout)
         
    return msgout # new_message['content']    


@app.route('/bot')
def bot():
    # check aiml
    myquery = request.args.get('query')
    
    msgaiml = filter(myquery)
    msgout = msgaiml
    if ((msgaiml == "poweroff") or msgaiml == "spegniti"):
        os.system("sudo poweroff")

    if msgaiml == "":
        # if key doesn't exist, returns None
        messages = [
            {"role": "system", "content": "Sei un assistente virtuale chiamata MARRtina e parli italiano."}
        ]
        

        messages.append({"role": "user", "content": myquery})
        new_message = get_response(messages=messages)
        messages.append(new_message)
        msgout = new_message['content']
        msgout = split_string(msgout)

    log_to_file(myquery,msgaiml,msgout)
        
    return msgout # new_message['content']
    
@app.route('/query')
def query():
    # if key doesn't exist, returns None
    myquery = request.args.get('query')
    message = get_response(messages=myquery)
    print(f"\nJOI: {new_message['content']}")

    return '''<h1>The language value is: {}</h1>'''.format(myquery)
    
@app.route('/form-example')
def form_example():
    return 'Form Data Example'

@app.route('/json')
def json():
    # if key doesn't exist, returns None
    messages = [
        {"role": "system", "content": "Sei un assistente virtuale chiamata MARRtina e parli italiano."}
    ]
    myquery = request.args.get('query')
    messages.append({"role": "user", "content": myquery})
    new_message = get_response(messages=messages)
    messages.append(new_message)
    msg = new_message['content']
    msgjson = {
        "response": msg,
        "action": "ok",
    }

    return jsonify(msgjson)
    

if __name__ == '__main__':
    # run app in debug mode on port 5000
    myip='10.3.1.1'
    app.run(host=myip,debug=True, port=5000)
