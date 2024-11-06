import azure.functions as func
import datetime
import json
import logging


app = func.FunctionApp()

# 1. Azure Function per il controllo della vaidità dell'url
@app.route(route="HttpExample", auth_level=func.AuthLevel.ANONYMOUS)
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    url_da_validare = req.params.get('url_da_validare')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    '''if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )'''
    if url_da_validare:
        url_valido = controllo_validita_url(url_da_validare)
        if url_valido:
            return func.HttpResponse(f"URL valido")
        else:
             return func.HttpResponse('URL non valido')
        
# 2. Azure function per estrazione parole chiave
# Caricare PDF e cercare parole chiave
import re
from pypdf import PdfReader
from io import BytesIO

@app.route(route="ricerca_keyword_pdf", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
def ricerca_keyword_pdf(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Endpoint ricerca_keyword_pdf è stato chiamato.")
    
    try:
        # Riceve il PDF come file binario
        file_bytes = req.get_body()

        # Parole chiave da cercare
        keywords = ["LD₅₀", "LD50", "LD 50", "Ld50", "Ld₅₀"]
        
        # Estrae il testo dal PDF
        testo_estratto = estrai_testo_pdf(BytesIO(file_bytes))

        # Ricerca delle parole chiave
        contesti_estratti = estrai_contesto(testo_estratto, keywords)

        # Concatenare i contesti estratti in una stringa
        risultato = "\n\n".join(contesti_estratti) if contesti_estratti else "Nessun contesto trovato."

        # Restituisce i contesti come HttpResponse
        return func.HttpResponse(
            risultato,
            mimetype="text/plain",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Errore durante l'elaborazione del PDF: {e}")
        return func.HttpResponse("Errore durante l'elaborazione della richiesta.", status_code=500)

    
# Funzioni    
def controllo_validita_url(url):
    return url.startswith('http://') or url.startswith('https://')


#Funzione per estrarre tutto il testo dai PDF
def estrai_testo_pdf(contenuto_pdf_binario):
    reader = PdfReader(contenuto_pdf_binario)
    lunghezza_pdf = len(reader.pages)
    testo_estratto = ""
    for pagina in range(lunghezza_pdf):
        oggetto_pagina = reader.pages[pagina]
        testo_estratto += oggetto_pagina.extract_text()
    return testo_estratto

# Funzione per estrarre contesto attorno alle parole chiave
def estrai_contesto(testo_estratto, keyword, context_lines=2):
    if testo_estratto is None:
        return []

    righe = testo_estratto.split('\n')
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)  #Permette di trovare la parola chiave comunque sia scritta

    risultati = []
    for i, riga in enumerate(righe):
        if pattern.search(riga):
            start = max(0, i - context_lines)
            end = min(len(righe), i + context_lines + 1)
            contesto = "\n".join(righe[start:end])
            contesto = pattern.sub(f"**{keyword}**", contesto)  #Parola chiave messa in grassetto
            risultati.append(contesto)
    return risultati