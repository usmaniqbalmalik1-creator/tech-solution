from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_health():
    assert client.get("/health").json()["status"]=="ok"

def test_create_and_get():
    r=client.post("/items",json={"name":"Async API","price":99,"tags":["fastapi"]})
    assert r.status_code==201
    item=r.json()
    assert client.get(f"/items/{item['id']}").status_code==200
