# 📝 FAST API Manual JWT (Notes Project)

## 📌 Project Overview
This project implements a complete, secured **Notes Application** featuring user authentication and CRUD (Create, Read, Update, Delete) operations on personal notes. It serves both as a RESTful backend and a static web client frontend.

A primary highlight of this project is the **Manual JWT Authentication system**. Instead of relying on higher-level automated authentication abstractions, this project implements a custom signature, serialization, and decoding flow (using `python-jose` and custom dependency injection) to demonstrate a deep understanding of cryptography and stateful session security.

---

## 🛠️ Tech Stack
* **Backend Framework**: FastAPI
* **Frontend**: HTML5, Vanilla CSS, JavaScript (served directly from the backend)
* **Database & ORM**: SQLite, SQLAlchemy
* **Security & Auth**: Custom JWT generation & Bearer Authentication dependencies (`python-jose`), Bcrypt password hashing (`passlib`)
* **Logging**: Python standard logging with custom rolling logs.

---

## 📂 Project Structure
```
FAST_API_Manual_JWT/
│
├── database/
│   └── database1.db              # Local SQLite database
│
├── Logs/
│   └── zlogger.py                # Rolling logger configuration
│
├── JWT_manual_auth_depends.py    # Custom dependency injection for fetching current user
├── JWT_manual_schema.py          # Pydantic schemas for request validation
├── JWT_manul_auth_utils.py       # Authentication helper utilities (hash checks, db deletion)
├── JWTmodels.py                  # SQLAlchemy entities (User and UserNotes tables)
├── Token.py                      # Custom JWT token builder and configuration
├── engine.py                     # SQLAlchemy session & database engine setup
├── index.html                    # Frontend Web UI (served at '/')
├── main.py                       # Server entry point and API definitions
├── requirements.txt              # Project dependencies
├── brand_icon.png                # Static asset
├── logo+notes_app.png            # Static asset
└── login.txt                     # Sample developer references
```

---

## 🚀 Installation & Setup

### 1. Clone & Navigate
```bash
cd FAST_API_Manual_JWT
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Server
```bash
python -m uvicorn main:app --port 8000 --reload
```
Open your browser and navigate to:
👉 **[http://localhost:8000](http://localhost:8000)** to interact with the web interface.

Interactive Swagger documentation is available at:
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 🔑 API Reference

### 1. Public Authentication Endpoints
* **User Signup**
  * `POST /signup`
  * Body: `{"username": "myusername", "mail": "user@gmail.com", "password": "mypassword"}`
  * Description: Hashes the password and registers the user.

* **User Login**
  * `POST /login`
  * Body: `{"mail": "user@gmail.com", "password": "mypassword"}`
  * Description: Verifies credentials and returns a custom-signed JWT Bearer token.

---

### 2. Secured Endpoints (Requires Authorization Header)
*All secured endpoints expect the header `Authorization: Bearer <token>`.*

* **Get Notes**
  * `GET /get_user_notes`
  * Description: Retrieves all notes owned by the authenticated user.

* **Write Note**
  * `POST /writeNote`
  * Body: `{"title": "My Title", "content": "My Note Content"}`
  * Description: Creates a new note.

* **Delete Note**
  * `DELETE /deleteNote`
  * Body: `{"title": "My Title"}`
  * Description: Deletes a note matching the title owned by the authenticated user.

* **Delete User Account**
  * `DELETE /delete?enter_pass={password}`
  * Description: Verifies password and permanently deletes the user account and associated notes.

---

## 🔒 Custom JWT & Security Design
* **Bcrypt Hashing**: Utilizes `passlib.context.CryptContext` with the `bcrypt` hashing scheme to ensure passwords are never stored in plain text.
* **Manual Signature**: Generates tokens using standard HMAC-SHA256 (`HS256`) algorithms. The token includes the subscriber claim (`sub`), issuance timestamp (`iat`), and expiration claim (`exp` - set to 10 minutes).
* **Dependency Injection**: Utilizes FastAPI's `Depends` system to inspect the HTTP `Authorization` header, parse out the credentials, verify the signature, validate expiration, and inject the authenticated user's email directly into the controller context.
