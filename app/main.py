
# importa a classe FastAPI do framework
# FastAPI é o framework backend. Ele vai receber requisições HTTP e gerar respostas.

from fastapi import FastAPI

# cria uma instância da aplicação FastAPI e guarda na variável app
# title:serve para configurar a documentação automática que o FastAPI gera (/docs e /redoc).
app = FastAPI(title="PedidoFácil Backend" )

@app.get("/health")
def health_check():
    return {"status": "ok"}