import json

def test_register_and_login(client):
    # Register new user
    res = client.post("/api/register", json={"username": "scott", "password": "pw"})
    assert res.status_code == 201
    assert "User created" in res.get_json()["message"]

    # Duplicate username
    res2 = client.post("/api/register", json={"username": "scott", "password": "pw"})
    assert res2.status_code == 400

    # Login
    res3 = client.post("/api/login", json={"username": "scott", "password": "pw"})
    data = res3.get_json()
    assert res3.status_code == 200
    assert "access_token" in data

    # Bad credentials
    res4 = client.post("/api/login", json={"username": "scott", "password": "wrong"})
    assert res4.status_code == 401
