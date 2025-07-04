# tests/test_post.py

from app.models import User

def test_create_post(client, app):
    client.post("/api/auth/register", json={
        "username": "poster",
        "email": "poster@example.com",
        "password": "posterpass"
    })

    res = client.post("/api/auth/login", json={
        "email": "poster@example.com",
        "password": "posterpass"
    })

    token = res.get_json()["access_token"]

    res = client.post("/api/posts/", json={
        "title": "Test Post",
        "content": "Test Content"
    }, headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 201
