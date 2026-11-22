import requests
import pandas as pd

BASE_URL = "http://localhost:8000"
page = 1


session = requests.Session()
session.headers["Authorization"] = "Bearer token-treino-123"

def get_requests(page):
    return session.get(
        f"{BASE_URL}/pedidos",
        params={"page": page, "per_page": 50},
        timeout=10
    )

result_list = []

response = get_requests(page)
while response.json()["data"] != []:
    data = response.json()["data"]
    for request in data:
        itens = request.pop("itens")
        total = 0
        for item in itens:
            total += item["quantidade"] * item["preco_unitario"]

        request["total"] = total
        result_list.append(request)

    
    page += 1
    response = get_requests(page)

result_df = pd.DataFrame(
    result_list
)

result_df.to_csv("result.csv")