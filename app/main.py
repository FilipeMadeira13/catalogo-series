from fastapi import FastAPI

from app.routers import serie

app = FastAPI()
app.include_router(serie.router)

@app.get('/')
def home():
    return {'mensagem': 'Catálogo de Séries em construção'}