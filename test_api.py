import requests
import json

BASE_URL = 'http://localhost:8000/api'

def test_register():
    url = f"{BASE_URL}/users/register/"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "password2": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    response = requests.post(url, json=data)
    print(f"Register Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_login():
    url = f"{BASE_URL}/users/login/"
    data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    response = requests.post(url, json=data)
    print(f"Login Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_create_liveblog(token):
    url = f"{BASE_URL}/liveblogs/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "Test LiveBlog",
        "content": "This is a test liveblog created via API",
        "event_status": "ONGOING"
    }
    response = requests.post(url, json=data, headers=headers)
    print(f"Create LiveBlog Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_get_liveblogs():
    url = f"{BASE_URL}/liveblogs/"
    response = requests.get(url)
    print(f"Get LiveBlogs Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_create_comment(token, liveblog_id):
    url = f"{BASE_URL}/liveblogs/{liveblog_id}/comments/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "content": "This is a test comment created via API"
    }
    response = requests.post(url, json=data, headers=headers)
    print(f"Create Comment Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def main():
    # Uncomment to register a new user
    # register_data = test_register()
    
    # Login to get token
    login_data = test_login()
    token = login_data.get("access")
    
    # Create a liveblog
    liveblog_data = test_create_liveblog(token)
    liveblog_id = liveblog_data.get("id")
    
    # Get all liveblogs
    test_get_liveblogs()
    
    # Create a comment on the liveblog
    test_create_comment(token, liveblog_id)

if __name__ == "__main__":
    main()