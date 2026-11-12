def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_status_endpoint(client):
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["api"] == "up"
    assert data["db"] == "connected"


def test_items_crud(client):
    # 1. Create item
    res = client.post("/api/v1/items", json={"name": "Widget A", "description": "High performance"})
    assert res.status_code == 201
    item = res.json()
    assert item["name"] == "Widget A"
    item_id = item["id"]

    # 2. Get item
    res = client.get(f"/api/v1/items/{item_id}")
    assert res.status_code == 200
    assert res.json()["name"] == "Widget A"

    # 3. List items
    res = client.get("/api/v1/items")
    assert res.status_code == 200
    items = res.json()
    assert len(items) >= 1
