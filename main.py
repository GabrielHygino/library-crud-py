from pymongo import MongoClient
from fastapi import FastAPI

app = FastAPI()
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["livraria"]
collections = mydb["livros"]

def livro_helper(livro) -> dict:
    return {
        "id": str(livro["_id"]),
        "name": livro["name"],
        "author": livro["author"],
        "gender": livro["gender"]
    }    

@app.get("/pega_livros")
def pega_livros():
    lista_livros = []
    for livro in collections.find():
        lista_livros.append(livro_helper(livro))
    return lista_livros

@app.put("/livro_add")
def livro_add(livro: str, autor:str, genero:str):
    collections.insert_one({"name":f"{livro}", "author":f"{autor}", "gender":f"{genero}"})
    return pega_livros()

@app.delete("/remove_livro")
def remove_livro(livro: str):
    collections.delete_many({"name":f"{livro}"})
    return pega_livros()
    