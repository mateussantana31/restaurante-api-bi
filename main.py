

import os
import secrets
from datetime import date
from fastapi import FastAPI, Header, HTTPException, Depends, Query

app = FastAPI(
    title="API Restaurante BI",
    version="2.0"
)

API_KEY = os.getenv("RESTAURANTE_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "Configure a variavel RESTAURANTE_API_KEY"
    )

def validar_api_key(
    x_api_key: str | None = Header(default=None)
):
    if not x_api_key or not secrets.compare_digest(
        x_api_key, API_KEY
    ):
        raise HTTPException(
            status_code=401,
            detail="Chave de API invalida ou ausente"
        )


produtos = [
    {"id_produto": 1, "nome": "Hamburguer", "categoria": "Lanches", "preco": 32.90},
    {"id_produto": 2, "nome": "Pizza", "categoria": "Pizzas", "preco": 59.90},
    {"id_produto": 3, "nome": "Refrigerante", "categoria": "Bebidas", "preco": 8.00},
    {"id_produto": 4, "nome": "Batata Frita", "categoria": "Porcoes", "preco": 19.90}
]

clientes = [
    {"id_cliente": 1, "nome": "Cliente A", "cidade": "Belo Horizonte"},
    {"id_cliente": 2, "nome": "Cliente B", "cidade": "Sabara"},
    {"id_cliente": 3, "nome": "Cliente C", "cidade": "Contagem"}
]

vendas = [
    {"id_venda": 101, "data_venda": "2026-10-25", "id_cliente": 1, "valor_total": 65.80, "status": "Concluida"},
    {"id_venda": 102, "data_venda": "2026-10-26", "id_cliente": 2, "valor_total": 59.90, "status": "Concluida"},
    {"id_venda": 103, "data_venda": "2026-10-27", "id_cliente": 3, "valor_total": 40.90, "status": "Concluida"},
    {"id_venda": 104, "data_venda": "2026-10-28", "id_cliente": 1, "valor_total": 19.90, "status": "Concluida"},
    {"id_venda": 105, "data_venda": "2026-10-29","id_cliente": 2,  "valor_total": 92.80, "status": "Concluida"}
]

itens_pedido = [
    {"id_venda": 101, "id_produto": 1, "quantidade": 2, "valor_unitario": 32.90},
    {"id_venda": 102, "id_produto": 2, "quantidade": 1, "valor_unitario": 59.90},
    {"id_venda": 103, "id_produto": 1, "quantidade": 1, "valor_unitario": 32.90},
    {"id_venda": 103, "id_produto": 3, "quantidade": 1, "valor_unitario": 8.00},
    {"id_venda": 104, "id_produto": 4, "quantidade": 1, "valor_unitario": 19.90},
    {
    "id_venda": 105,
    "id_produto": 1,
    "quantidade": 1,
    "valor_unitario": 32.90
},
{
    "id_venda": 105,
    "id_produto": 2,
    "quantidade": 1,
    "valor_unitario": 59.90
}
]

@app.get("/")
def inicio():
    return {"mensagem": "API Restaurante funcionando"}


@app.get("/api/v1/produtos")
def listar_produtos(
    autorizado=Depends(validar_api_key)
):
    return produtos


@app.get("/api/v1/clientes")
def listar_clientes(
    autorizado=Depends(validar_api_key)
):
    return clientes



@app.get("/api/v1/vendas")
def listar_vendas(
    pagina: int = Query(default=1, ge=1),
    limite: int = Query(default=100, ge=1, le=1000),
    data_inicio: date | None = None,
    data_fim: date | None = None,
    autorizado=Depends(validar_api_key)
):
    if data_inicio and data_fim and data_inicio > data_fim:
        raise HTTPException(
            status_code=400,
            detail="data_inicio nao pode ser maior que data_fim"
        )

    resultado = vendas.copy()

    if data_inicio:
        resultado = [
            v for v in resultado
            if date.fromisoformat(v["data_venda"]) >= data_inicio
        ]

    if data_fim:
        resultado = [
            v for v in resultado
            if date.fromisoformat(v["data_venda"]) <= data_fim
        ]

    resultado.sort(key=lambda v: v["id_venda"])

    total = len(resultado)
    inicio = (pagina - 1) * limite
    fim = inicio + limite

    registros = resultado[inicio:fim]

    return {
        "pagina": pagina,
        "limite": limite,
        "total_registros": total,
        "total_paginas": (total + limite - 1) // limite,
        "dados": registros
    }



@app.get("/api/v1/itens-pedido")
def listar_itens(
    autorizado=Depends(validar_api_key)
):
    return itens_pedido

