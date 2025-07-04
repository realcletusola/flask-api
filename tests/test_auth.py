def test_register_and_login(client):
    # Register
    res = client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass"
    })
    assert res.status_code == 201

    # Login
    res = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "testpass"
    })
    assert res.status_code == 200
    assert "access_token" in res.get_json()
