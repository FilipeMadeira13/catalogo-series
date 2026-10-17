from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return {'mensagem': 'Catálogo de Séries em construção'}