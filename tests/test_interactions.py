def test_create_comment(client):
    # 1. Регистрируем пользователя
    client.post(
        "/users/",
        json={"username": "commentuser", "password": "password123"}
    )
    
    # 2. Получаем токен
    login_response = client.post(
        "/token",
        data={"username": "commentuser", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    # 3. Создаем пост, чтобы было куда писать комментарий
    post_response = client.post(
        "/posts/",
        json={"title": "Post for comments", "content": "Content"},
        headers={"Authorization": f"Bearer {token}"}
    )
    post_id = post_response.json()["id"]
    
    # 4. Создаем комментарий к этому посту
    response = client.post(
        f"/posts/{post_id}/comments",
        json={"text": "This is a great test comment!"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "This is a great test comment!"
    assert data["post_id"] == post_id

def test_toggle_like(client):
    # 1. Регистрируем пользователя и получаем токен
    client.post(
        "/users/",
        json={"username": "likeuser", "password": "password123"}
    )
    login_response = client.post(
        "/token",
        data={"username": "likeuser", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    # 2. Создаем пост
    post_response = client.post(
        "/posts/",
        json={"title": "Post for likes", "content": "Content"},
        headers={"Authorization": f"Bearer {token}"}
    )
    post_id = post_response.json()["id"]
    
    # 3. Ставим лайк первый раз
    response = client.post(
        f"/posts/{post_id}/like",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Post liked successfully"
    
    # 4. Отправляем запрос второй раз (лайк должен сняться)
    response_unliked = client.post(
        f"/posts/{post_id}/like",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response_unliked.status_code == 200
    assert response_unliked.json()["message"] == "Like removed successfully"