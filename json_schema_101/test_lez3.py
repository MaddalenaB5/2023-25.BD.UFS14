#lanciando dal terminale il comando pytest si vanno a cercare i file nella cartella con la parola 'test' all'interno

from jsonschema import validate

schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
    },
}


def func(x):
    return x + 1


def test_answer():
    assert func(4) == 5


def test_jschema_success():
    validate(instance={"name" : "Eggs", "price" : 34.99}, schema=schema)

def test_validation():
    assert validate_wrapper(instance={"name" : "Eggs", "price" : 34.99}, schema=schema) == True

def test_validation_fail():
    assert validate_wrapper(instance={"name" : "Eggs", "price" : 'Ciao'}, schema=schema) == False

# creo un decoratore perchè la funzione con validate restituisce solo un 'none' e non un booleano T F che ci sarebbe molto più utile
def validate_wrapper(instance, schema):
    try:
        validate(instance= instance, schema= schema)
        return True # qui il none diventa true
    except:
        return False # qui l'errore che dava altrimenti diventa false


#test usando snapshot
def test_function_output_with_snapshot(snapshot):
    snapshot.snapshot_dir = 'snapshots'
    pierino = str(func(12))
    snapshot.assert_match(pierino, 'foo_output.txt')


a = '''frutti,prezzo,colore,sapore
pera,100,rossa,buona
mela,10,blu,squisita
ananas,23,turchino,piccante
'''

def test_function_output_with_snapshot(snapshot):
    snapshot.snapshot_dir = 'snapshots'
    andrea = a
    snapshot.assert_match(andrea, 'foo_output.csv')