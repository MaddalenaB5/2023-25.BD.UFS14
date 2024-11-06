import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()


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

     

def controllo_validita_url(url):
    return url.startswith('http://') or url.startswith('https://') 


