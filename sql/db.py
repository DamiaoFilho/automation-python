import sqlite3
from pathlib import Path

DB = BASE_DIR = Path(__file__).parent / "loja.db"

with sqlite3.connect(DB) as conn:
    # rows = conn.execute(
    #     "SELECT status, COUNT(*) FROM pedidos group by status"
    # ).fetchall()
    # print(rows)

    # rows = conn.execute(
    #     """
    #     SELECT c.nome, SUM(ip.quantidade * ip.preco_unitario) as total FROM clientes c
    #         INNER JOIN pedidos p on c.id = p.cliente_id
    #         INNER JOIN itens_pedido ip on p.id = ip.pedido_id
    #         INNER JOIN produtos pd ON pd.id = ip.produto_id
    #         WHERE p.status IN ('entregue', 'enviado') 
    #         GROUP BY c.id
    #         ORDER BY total DESC
    #         LIMIT 5;
    #     """
    # ).fetchall()
    # print(rows)

    # rows = conn.execute(
    #     """
    #     SELECT c.nome, c.id from clientes c
    #         LEFT JOIN pedidos p ON c.id = p.cliente_id
    #         WHERE p.id IS NULL
    #     """
    # ).fetchall()
    # print(rows)

    rows = conn.execute(
        """
        SELECT p.categoria, SUM(ip.quantidade) as quantidade, ROUND(SUM(ip.quantidade * ip.preco_unitario), 2) as valor_total FROM itens_pedido ip
            inner JOIN produtos p on ip.produto_id = p.id
            INNER JOIN pedidos pd on pd.id = ip.pedido_id
            WHERE pd.status in ('enviado', 'entregue')
            GROUP BY p.categoria
        """
    ).fetchall()
    print(rows)

