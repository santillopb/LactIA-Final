from fastapi import FastAPI, Query
from script import devRespuesta
app = FastAPI()

@app.get("/")
def read_root():
    dict = {"Hello" : "World"}
    return dict["Hello"]

@app.post("/")
def read_root(question: str = Query(..., min_length=3)):
    # Conectamos con el modelo y nos devuelve una respuesta
    #muestraPregunta()
    dict = {"Hello" : "World"}
    print(question)
    return  devRespuesta(question)

