📘 API Documentation

🚀 Getting Started
🧾 Clone the Repository
```
git clone https://github.com/realcletusola/flask-api.git
cd to the repo name ( cd flask-api)
```

📦 Install Requirements

It's recommended to use a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

```

⚙️ Environment Variables

Create a .env file in the project root (or export manually):

FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost/dbname
JWT_SECRET_KEY=your_jwt_secret

🗃️ Run Database Migrations

```
flask db init      # Only once
flask db migrate -m "Initial migration"
flask db upgrade

```

▶️ Run the Application

flask run


🔐 Authentication

All protected routes require a JWT token in the Authorization header:

Authorization: Bearer <access_token>

🧑‍💻 User Endpoints
✅ Register

POST /api/auth/register

Request Body:
```
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepass"
}

```

Response:
```
{
  "message": "User registered successfully"
}
```

🔐 Login

POST /api/auth/login

Request Body:
```
{
  "email": "john@example.com",
  "password": "securepass"
}
```
Response:
```
{
  "message": "Login successful",
  "access_token": "<JWT_TOKEN>"
}
```

📝 Post Endpoints

📄 Get All Posts (Paginated)

GET /api/posts/?page=1&per_page=10

Response:
```
{
  "total": 42,
  "pages": 5,
  "current_page": 1,
  "per_page": 10,
  "next": 2,
  "prev": null,
  "items": [
    {
      "id": 1,
      "title": "First Post",
      "content": "Hello world",
      "user_id": 1
    },
    ...
  ]
}
```

🆕 Create Post

POST /api/posts/
Auth required

Request Headers:
Authorization: Bearer <access_token>

Request Body:
```
{
  "title": "New Post",
  "content": "This is the content of the post"
}
```
Response:
```
{
  "message": "Post created successfully",
  "id": 15
}
```
⚠️ Error Responses (Common)

401 Unauthorized:
```
{
  "msg": "Missing Authorization Header"
}

```
422 Unprocessable Entity:
```
{
  "msg": "Subject must be a string"
}
```

400 Bad Request:
```
{
  "message": "Title and content are required"
}
```

🧪 Running Tests

pytest
