from app import app

def test_index():
    client = app.test_client()
    response = client.get(
        "/login",
        content_type="html/text"
    )
    assert response.status_code == 200
    assert "text/html" in response.content_type
