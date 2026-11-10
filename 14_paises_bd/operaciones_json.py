import json
def continentes():
    with open ("countries.json","r") as f:
        return list(set(map(lambda p:p["region"],json.load(f))))
    
def paises():
   with open ("countries.json","r") as f:
        return json.load(f) 
    