# Blog API

A RESTful API for a blog platform that allows users to manage blog posts, comments, and user authentication. The API is built using Flask, SQLAlchemy, and Flask-JWT-Extended for authentication.

## Features

- **User Authentication**: Register, login, and manage users using JWT for secure access.
- **Blog Posts Management**: Create, retrieve, update, and delete blog posts.
- **Comments Management**: Add, retrieve, update, and delete comments on blog posts.
- **Pagination**: Paginate through blog posts and comments.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/) (or another database supported by SQLAlchemy)

## Installation

1. **Clone the repository**:
```bash
   git clone https://github.com/fazzy12/blogy.git
   cd api
 ```

2. **Set up a virtual environment**:

```
python3 -m venv venv
```

3. Activate the virtual environment:

- **On Windows**:

```
venv\Scripts\activate
```

- **On macOS/Linux**:
```
source venv/bin/activate
```

4. Install dependencies:

```
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root directory of your project and add the following environment variables:

```
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://username:password@localhost:5432/blog_db
```

- **FLASK_ENV**: Set to development for development purposes.
- **SECRET_KEY**: A secret key for signing JWT tokens.
- `**DATABASE_URL**: The URL of your PostgreSQL database.

## Database Setup

1. Create the database:
```
createdb blog_db
```

2. Apply database migrations with Alembic:

Alembic is used for handling database migrations. Follow these steps to set it up and run migrations:

- **Initialize Alembic** (only if you haven't already):
    ```
    alembic init alembic
    ```

    This will create an `alembic` directory with necessary configuration files.

- **Configure Alembic**:

    In the `alembic.ini` file, set your `SQLALCHEMY_DATABASE_URL` in the `env.py` file under alembic:

- **Generate a migration**:

    ```
    alembic revision --autogenerate -m "Initial migration"
    ```
    This will generate a new migration script based on your models.

- **Apply the migration**:
    ```
    alembic upgrade head
    ```
## Running the Application

To start the development server, run:

```
python3 api/app.py
```
The application will be available at `http://127.0.0.1:5000/`.

## API Endpoints
### Users
- Create a User
    ```
    POST /api/v1/users
    ```

- Get All Users

    ```
    GET /api/v1/users
    ```

- Get a Single User

    ```
    GET /api/v1/users/<string:user_id>

    ```

- Update a User

    ```
    PUT /api/v1/users/<string:user_id>

    ```

- Delete a User

    ```
    DELETE /api/v1/users/<string:user_id>
    ```
### login
-  login the user
    ```
    POST /api/v1/login
    ```

### Blog Posts
- Create a Blog Post
    ```
    POST /api/v1/blog_posts
    ```
- Get All Blog Posts
    ```
    GET /api/v1/blog_posts
    ```
- Get a Single Blog Post
    ```
    GET /api/v1/blog_posts/<string:post_id>
    ```
- Update a Blog Post
    ```
    PUT /api/v1/blog_posts/<string:post_id>
    ```
- Delete a Blog Post
    ```
    DELETE /api/v1/blog_posts/<string:post_id>
    ```
### Comments
- Create a Comment
    ```
    POST /api/v1/comments
    ```
- Get Comments for a Blog Post
    ```
    GET /api/v1/blog_posts/<string:post_id>/comments
    ```
- Get a Single Comment
    ```
    GET /api/v1/comments/<string:comment_id>
    ```
- Update a Comment
    ```
    PUT /api/v1/comments/<string:comment_id>
    ```
- Delete a Comment
    ```
    DELETE /api/v1/comments/<string:comment_id>
    ```

## Testing

To run the tests, use the following command:

```
pytest
```
Tests are located in the tests directory and cover all key functionalities of the API.








