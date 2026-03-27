# :pencil: Masterblog API - Flask Blog REST API

**Full-Stack Blog Application with REST Backend and Flask Frontend**

A two-server Flask application to manage blog posts via a REST API.
Create, update, delete and search posts through a clean web interface,
with full sorting and filtering support.

## :sparkles: Features

- **CRUD Operations**: Add, update and delete blog posts via REST API
- **Sorting**: Sort posts by title or content, ascending or descending
- **Search**: Filter posts by title and/or content (substring match)
- **Input Validation**: Descriptive error responses for missing or invalid parameters
- **CORS enabled**: Frontend and backend run on separate ports
- **In-memory Storage**: Posts are stored in memory at runtime

## :file_folder: Project Structure

```
Masterblog-API/
├── backend/
│   └── backend_app.py
├── frontend/
│   ├── static/
│   │   ├── main.js
│   │   └── style.css
│   ├── templates/
│   │   └── index.html
│   └── frontend_app.py
├── README.md
└── requirements.txt

```

## :wrench: Setup & Usage

1. **Clone the repository**  
`git clone ...`
2. **Install virtual env**  
Windows: `python -m venv .venv`  
Linux / macOS: `python3 -m venv .venv`
3. **Install dependencies**  
Windows: `pip install -r requirements.txt`  
Linux / macOS: `pip3 install -r requirements.txt`
4. **Start the backend**  
Windows: `python backend_app.py`  
Linux / macOS: `python3 backend_app.py`
5. **Start the frontend** (separate terminal)  
Windows: `python frontend_app.py`  
Linux / macOS: `python3 frontend_app.py`
6. **Open in browser**  
`http://127.0.0.1:5001`

>**Note:** The update functionality (PATCH) is only available directly
> via the REST API at `http://127.0.0.1:5002/api/posts/<id>` and is not
> implemented in the frontend UI.

## :clipboard: API Endpoints

| Route                      | Method   | Description                                         |
|----------------------------|----------|-----------------------------------------------------|
| `/api/posts`               | GET      | Get all posts (supports `?sort=` and `?direction=`) |
| `/api/posts`               | POST     | Create a new post                                   |
| `/api/posts/<int:post_id>` | PATCH    | Update title and/or content of a post               |
| `/api/posts/<int:post_id>` | DELETE   | Delete a post by ID                                 |
| `/api/posts/search`        | GET      | Search posts by `?title=` and/or `?content=`        |

## :mag: Query Parameters

**Sorting** – `GET /api/posts`

| Parameter   | Values             | Description                     |
|-------------|--------------------|---------------------------------|
| `sort`      | `title`, `content` | Field to sort by                |
| `direction` | `asc`, `desc`      | Sort order (default: ascending) |

**Search** – `GET /api/posts/search`

| Parameter  | Description                         |
|------------|-------------------------------------|
| `title`    | Filter by title (substring match)   |
| `content`  | Filter by content (substring match) |

## :package: Dependencies

`flask` - web framework for routing and templates  
`flask-cors` - enables Cross-Origin Resource Sharing between frontend and backend














