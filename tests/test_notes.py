def register_and_login(client, username="user1", password="pw"):
    client.post("/api/register", json={"username": username, "password": password})
    res = client.post("/api/login", json={"username": username, "password": password})
    return res.get_json()["access_token"]

def test_create_and_get_notes(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create note
    res = client.post("/api/1/notes", json={"text": "Buy milk"}, headers=headers)
    assert res.status_code == 201
    note_id = res.get_json()["note"]["id"]

    # Retrieve notes
    res2 = client.get("/api/1/notes", headers=headers)
    assert res2.status_code == 200
    assert any("Buy milk" in n["text"] for n in res2.get_json()["notes"])

    # Update
    res3 = client.put(f"/api/1/notes/{note_id}", json={"text": "Buy oat milk"}, headers=headers)
    assert res3.status_code == 200
    assert res3.get_json()["text"] == "Buy oat milk"

    # Delete
    res4 = client.delete(f"/api/1/notes/{note_id}", headers=headers)
    assert res4.status_code == 204

def test_unauthorized_access(client):
    token1 = register_and_login(client, "alice")
    token2 = register_and_login(client, "bob")
    headers1 = {"Authorization": f"Bearer {token1}"}
    headers2 = {"Authorization": f"Bearer {token2}"}

    # Alice creates note
    client.post("/api/1/notes", json={"text": "secret"}, headers=headers1)

    # Bob tries to read Alice's notes (should fail)
    res = client.get("/api/1/notes", headers=headers2)
    assert res.status_code == 403
