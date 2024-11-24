from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
from typing import List, Optional
from datetime import datetime

app = FastAPI()

class Cliente(BaseModel):
    nome: constr(max_length=50)
    tipo_atendimento: constr(max_length=1)
    data_chegada: datetime
    atendido: bool

fila = []

@app.get("/fila", response_model=List[Cliente])
async def get_fila():
    fila_nao_atendida = [cliente for cliente in fila if not cliente.atendido]
    return fila_nao_atendida

@app.get("/fila/{id}", response_model=Cliente)
async def get_cliente(id: int):
    if id < 0 or id >= len(fila):
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return fila[id]

@app.post("/fila")
async def add_cliente(cliente: Cliente):
    if cliente.tipo_atendimento not in ["N", "P"]:
        raise HTTPException(status_code=400, detail="Tipo de atendimento deve ser 'N' ou 'P'")
    cliente.data_chegada = datetime.now()
    cliente.atendido = False
    fila.append(cliente)
    return {"message": "Cliente adicionado com sucesso"}

@app.put("/fila")
async def update_fila(): 
    global fila 
    nova_fila = [] 
    for i in range(len(fila)): 
        if i == 0: 
            fila[i].atendido = True  
        if not fila[i].atendido: 
            nova_fila.append(fila[i])  
    fila = nova_fila 
    return {"message": "Fila atualizada com sucesso"}

@app.delete("/fila/{id}")
async def delete_cliente(id: int):
    if id < 0 or id >= len(fila):
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    del fila[id]
    
    return {"message": "Cliente removido com sucesso"}
