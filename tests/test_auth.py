def test_create_user(client):
    response = client.post(
        "/users/",
        json={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

def test_login_and_get_token(client):
    # Сначала создаем пользователя
    client.post(
        "/users/",
        json={"username": "testuser", "password": "password123"}
    )
    
    # Пытаемся залогиниться (OAuth2PasswordRequestForm ожидает данные через form-data)
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"