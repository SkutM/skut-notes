def test_token_refresh_flow(client):
    # Register + login
    client.post("/api/register", json={"username": "alex", "password": "pw"})
    res = client.post("/api/login", json={"username": "alex", "password": "pw"})
    data = res.get_json()

    access = data["access_token"]
    refresh = data["refresh_token"]

    # Use refresh token to get new access
    res2 = client.post("/api/refresh", headers={"Authorization": f"Bearer {refresh}"})
    assert res2.status_code == 200
    new_access = res2.get_json()["access_token"]
    assert new_access != access
