import bard_api

# Richiedi la risposta di Bard a una query
def ask_bard(query):
    response = bard_api.generate(query)
    return response

# Genera un testo
response = ask_bard("Qual è il significato della vita?")
print(response)
