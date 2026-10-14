def test_create_post(client):
    # 1. Регистрируем пользователя
    client.post(
        "/users/",
        json={"username": "postuser", "password": "password123"}
    )
    
    # 2. Получаем токен для этого пользователя
    login_response = client.post(
        "/token",
        data={"username": "postuser", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    # 3. Создаем пост, передавая токен в заголовках (Authorization: Bearer <token>)
    response = client.post(
        "/posts/",
        json={"title": "First Test Post", "content": "Test content here"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "First Test Post"
    assert data["content"] == "Test content here"
    assert "id" in data

def test_get_posts(client):
    # Проверяем получение пустого списка постов по умолчанию
    response = client.get("/posts/")
    assert response.status_code == 200
    assert response.json() == []