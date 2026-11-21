import requests
import sqlite3
import csv

API = "http://localhost:8000"
TOKEN = "token-treino-123"


def buscar_pedidos(cliente_id, ids=[]):
    r = requests.get(API + "/pedidos?page=1&per_page=50",
                     headers={"Authorization": "Bearer " + TOKEN})
    dados = r.json()["data"]
    for p in dados:
        if p["cliente_id"] == cliente_id:
            ids.append(p["id"])
    return ids


def total_pedido(pedido):
    total = 0
    for item in pedido["itens"]:
        total = total + item["quantidade"] * item["preco_unitario"]
    return total


def salvar_resumo(nome_cliente, pedidos):
    con = sqlite3.connect("loja.db")
    cur = con.cursor()
    cur.execute("SELECT id FROM clientes WHERE nome = '" + nome_cliente + "'")
    cliente = cur.fetchone()
    f = open("resumo.csv", "w")
    w = csv.writer(f)
    for p in pedidos:
        try:
            w.writerow([cliente[0], p["id"], total_pedido(p)])
        except:
            pass
    print("resumo salvo para", nome_cliente)


if __name__ == "__main__":
    ids = buscar_pedidos(3)
    print(ids)
