# LiveBlog API Documentation

## Authentication

### Register a new user
- **URL**: `/api/users/register/`
- **Method**: `POST`
- **Auth required**: No
- **Permissions**: None
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "password2": "string",
    "first_name": "string",
    "last_name": "string"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "user": {
      "id": "integer",
      "username": "string",
      "email": "string",
      "first_name": "string",
      "last_name": "string",
      "bio": "string",
      "profile_picture": "string"
    },
    "refresh": "string",
    "access": "string"
  }
  ```

### Login
- **URL**: `/api/users/login/`
- **Method**: `POST`
- **Auth required**: No
- **Permissions**: None
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "refresh": "string",
    "access": "string"
  }
  ```

### Refresh Token
- **URL**: `/api/users/token/refresh/`
- **Method**: `POST`
- **Auth required**: No
- **Permissions**: None
- **Request Body**:
  ```json
  {
    "refresh": "string"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "access": "string"
  }
  ```

### Logout
- **URL**: `/api/users/logout/`
- **Method**: `POST`
- **Auth required**: Yes
- **Permissions**: Authenticated
- **Request Body**:
  ```json
  {
    "refresh": "string"
  }
  ```
- **Success Response**: `205 Reset Content`

## User Profile

### Get User Profile
- **URL**: `/api/users/profile/`
- **Method**: `GET`
- **Auth required**: Yes
- **Permissions**: Authenticated
- **Success Response**: `200 OK`
  ```json
  {
    "id": "integer",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "profile_picture": "string"
  }
  ```

### Update User Profile
- **URL**: `/api/users/profile/update/`
- **Method**: `PATCH`
- **Auth required**: Yes
- **Permissions**: Authenticated
- **Request Body**:
  ```json
  {
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "profile_picture": "string"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "profile_picture": "string"
  }
  ```

## LiveBlogs

### List LiveBlogs
- **URL**: `/api/liveblogs/`
- **Method**: `GET`
- **Auth required**: No
- **Permissions**: None
- **Query Parameters**:
  - `search`: Search in title and content
  - `ordering`: Order by field (e.g., timestamp, -timestamp)
  - `page`: Page number
- **Success Response**: `200 OK`
  ```json
  {
    "count": "integer",
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": "integer",
        "title": "string",
        "content": "string",
        "author": "string",
        "author_id": "integer",
        "timestamp": "datetime",
        "updated_at": "datetime",
        "event_status": "string",
        "comments_count": "integer"
      }
    ]
  }
  ```

### Create LiveBlog
- **URL**: `/api/liveblogs/`
- **Method**: `POST`
- **Auth required**: Yes
- **Permissions**: Authenticated
- **Request Body**:
  ```json
  {
    "title": "string",
    "content": "string",
    "event_status": "string"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "id": "integer",
    "title": "string",
    "content": "string",
    "author": "string",
    "author_id": "integer",
    "timestamp": "datetime",
    "updated_at": "datetime",
    "event_status": "string",
    "comments_count": "integer"
  }
  ```

### Get LiveBlog Detail
- **URL**: `/api/liveblogs/{id}/`
- **Method**: `GET`
- **Auth required**: No
- **Permissions**: None
- **Success Response**: `200 OK`
  ```json
  {
    "id": "integer",
    "title": "string",
    "content": "string",
    "author": "string",
    "author_id": "integer",
    "timestamp": "datetime",
    "updated_at": "datetime",
    "event_status": "string",
    "comments_count": "integer",
    "comments": [
      {
        "id": "integer",
        "content": "string",
        "author": "string",
        "timestamp": "datetime"
      }
    ]
  }
  ```

### Update LiveBlog
- **URL**: `/api/liveblogs/{id}/`
- **Method**: `PUT`
- **Auth required**: Yes
- **Permissions**: Author only
- **Request Body**:
  ```json
  {
    "title": "string",
    "content": "string",
    "event_status": "string"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "id": "integer",
    "title": "string",
    "content": "string",
    "author": "string",
    "author_id": "integer",
    "timestamp": "datetime",
    "updated_at": "datetime",
    "event_status": "string",
    "comments_count": "integer",
    "comments": [
      {
        "id": "integer",
        "content": "string",
        "author": "string",
        "timestamp": "datetime"
      }
    ]
  }
  ```

### Delete LiveBlog
- **URL**: `/api/liveblogs/{id}/`
- **Method**: `DELETE`
- **Auth required**: Yes
- **Permissions**: Author or Admin
- **Success Response**: `204 No Content`

### Update LiveBlog Status
- **URL**: `/api/liveblogs/{id}/status/`
- **Method**: `PATCH`
- **Auth required**: Yes
- **Permissions**: Author only
- **Request Body**:
  ```json
  {
    "event_status": "string"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "id": "integer",
    "title": "string",
    "content": "string",
    "author": "string",
    "author_id": "integer",
    "timestamp": "datetime",
    "updated_at": "datetime",
    "event_status": "string",
    "comments_count": "integer"
  }
  ```

### List User's LiveBlogs
- **URL**: `/api/my-liveblogs/`
- **Method**: `GET`
- **Auth required**: Yes
- **Permissions**: Authenticated
- **Success Response**: `200 OK`
  ```json
  {
    "count": "integer",
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": "integer",
        "title": "string",
        "content": "string",
        "author": "string",
        "author_id": "integer",
        "timestamp": "datetime",
        "updated_at": "datetime",
        "event_status": "string",
        "comments_count": "integer"
      }
    ]
  }
  ```

## Comments

### List Comments for a LiveBlog
- **URL**: `/api/liveblogs/{liveblog_id}/comments/`
- **Method**: `GET`
- **Auth required**: No
- **Permissions**: None
- **Success Response**: `200 OK`
  ```json
  {
    "count": "integer",
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": "integer",
        "content": "string",
        "author": "string",
        "timestamp": "datetime"
      }
    ]
  }
  ```

### Create Comment
- **URL**: `/api/liveblogs/{liveblog_id}/comments/`
- **Method**: `POST`
- **Auth required**: Yes
- **Permissions**: Authenticated
- **Request Body**:
  ```json
  {
    "content": "string"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "id": "integer",
    "content": "string",
    "author": "string",
    "timestamp": "datetime"
  }
  ```

### Get Comment Detail
- **URL**: `/api/comments/{id}/`
- **Method**: `GET`
- **Auth required**: No
- **Permissions**: None
- **Success Response**: `200 OK`
  ```json
  {
    "id": "integer",
    "content": "string",
    "author": "string",
    "timestamp": "datetime",
    "liveblog": "integer"
  }
  ```

### Update Comment
- **URL**: `/api/comments/{id}/`
- **Method**: `PUT`
- **Auth required**: Yes
- **Permissions**: Author only
- **Request Body**:
  ```json
  {
    "content": "string"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "id": "integer",
    "content": "string",
    "author": "string",
    "timestamp": "datetime",
    "liveblog": "integer"
  }
  ```

### Delete Comment
- **URL**: `/api/comments/{id}/`
- **Method**: `DELETE`
- **Auth required**: Yes
- **Permissions**: Author or Admin
- **Success Response**: `204 No Content`

## WebSocket Endpoints

### LiveBlog WebSocket
- **URL**: `ws://domain/ws/liveblog/{liveblog_id}/`
- **Auth required**: Yes (via token in query parameter)
- **Events**:
  - **Connect**: Connect to the LiveBlog channel
  - **Receive**: Receive updates for the LiveBlog
    ```json
    {
      "type": "liveblog_update",
      "liveblog": {
        "id": "integer",
        "title": "string",
        "content": "string",
        "author": "string",
        "event_status": "string",
        "timestamp": "datetime"
      }
    }
    ```
  - **Receive**: Receive new comments
    ```json
    {
      "type": "comment",
      "comment": {
        "id": "integer",
        "content": "string",
        "author": "string",
        "timestamp": "datetime"
      }
    }
    ```
  - **Send**: Add a new comment
    ```json
    {
      "type": "comment",
      "content": "string"
    }
    ```
  - **Send**: Update the LiveBlog (author only)
    ```json
    {
      "type": "liveblog_update",
      "title": "string",
      "content": "string",
      "event_status": "string"
    }
    ```