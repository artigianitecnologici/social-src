#!/usr/bin/python3

#modificato da francesco cirinei

def converti_dialogo_in_aiml(dialogo):
    aiml_content = "<aiml version='1.0'>\n"
    
    for linea in dialogo.split('\n'):
        if linea.startswith("user:"):
            pattern = "<pattern>{}</pattern>".format(linea.replace("user:", "").strip().upper())
        elif linea.startswith("bot:"):
            template = "<template>{}</template>".format(linea.replace("bot:", "").strip())
            category = "<category>\n{}\n{}\n</category>\n".format(pattern, template)
            aiml_content += category
    
    aiml_content += "</aiml>"
    return aiml_content

dialogo = """
user:chi e' paperino
bot:Paperino è un personaggio dei fumetti e dei cartoni animati creato da Walt Disney
user: Chi è Napoleone
bot: Napoleone Bonaparte è stato un generale e politico francese, nonché uno dei più importanti personaggi della storia mond
user: cosa ti piace fare?
bot: mi piace fare tante cose, ma la cosa che mi entusiasma di piu e parlare con le persone e interagire con loro. 
"""

aiml_output = converti_dialogo_in_aiml(dialogo)
with open("dialogo.aiml", "w") as file:
    file.write(aiml_output)

print("File AIML creato con successo!")
