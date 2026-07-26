# 📝 FastNote — FastAPI Manual JWT Notes Application

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg?style=flat&logo=sqlite)](https://www.sqlite.org/)
[![JWT](https://img.shields.io/badge/Auth-Manual%20JWT%20(hmac%20%2B%20hashlib)-black.svg?style=flat&logo=jsonwebtokens)](https://jwt.io/)
[![Frontend](https://img.shields.io/badge/Frontend-Vanilla%20HTML5%2FCSS3%2FJS-orange.svg?style=flat&logo=html5)](https://developer.mozilla.org/en-US/)

A high-performance, full-stack **Notes Application** featuring a **manual JWT authentication system** built with FastAPI and a modern **Glassmorphism Single-Page Application (SPA)** frontend served directly by the backend.

Designed for security, speed, and portfolio presentation, this project demonstrates custom signature serialization, stateful session handling, XSS-sanitized Markdown note editing, live search, and account management.

---

## 🌟 Key Features

### 🎨 Premium Glassmorphic UI/UX
- **SaaS-Grade Design**: Built using custom HSL design tokens, ambient backdrop blur (`backdrop-filter: blur(16px)`), crisp dark mode styling, and smooth micro-animations.
- **Typography & Icons**: Styled with Google Fonts (*Plus Jakarta Sans* and *JetBrains Mono*) and crisp inline SVG icons.
- **Responsive Workspace**: Seamless collapsible sidebar navigation optimized across Desktop, Tablet, and Mobile viewports.

### ✍️ Advanced Note Editor & Live Markdown
- **Live Preview & Split View**: Instant side-by-side or tabbed Markdown rendering powered by `marked.js` and sanitized via `DOMPurify` to prevent XSS attacks.
- **Real-Time Note Metrics**: Automatic calculation of word count, character count, and estimated reading time.
- **Save & Dirty State Indicators**: Visual badges (`Unsaved changes`, `Saving...`, `Saved`) notifying users of unsaved edits.
- **Keyboard Shortcuts**:
  - `Ctrl + S` / `Cmd + S` → Save active note
  - `Ctrl + N` / `Cmd + N` → Create new note
  - `Ctrl + P` / `Cmd + P` → Toggle Markdown Preview
  - `Esc` → Close modal dialogs / clear search

### 🔍 Debounced Instant Search
- High-performance live filtering across note titles and body content.
- Highlights matching search queries inline with match counter feedback.

### 🛡️ Manual JWT Security & Session Management
- **Manual Signature Construction**: Custom token builder using Python standard libraries (`hmac` and `hashlib`) with HMAC-SHA256 (`HS256`), subscriber (`sub`), issued-at (`iat`), and 10-minute expiration (`exp`) claims.
- **FastAPI Dependency Injection**: Auth verification performed inside `get_current_user` dependency, validating HTTP `Authorization: Bearer <token>` headers without high-level library abstractions.
- **Tab-Scoped Session Security**: Tokens stored safely in `sessionStorage` (cleared on tab close).
- **Two-Step Account Deletion**: Modal requires typing `DELETE` + password verification to invoke `DELETE /delete`.

---

## 🏗️ Architecture Overview

```
                          ┌────────────────────────┐
                          │   FastAPI Web Server   │
                          └───────────┬────────────┘
                                      │
              ┌───────────────────────┴───────────────────────┐
              │                                               │
   ┌──────────▼───────────┐                       ┌───────────▼───────────┐
   │  Static UI Engine    │                       │   REST API Controllers│
   │  (GET / -> index.html│                       │ (/signup, /login, etc)│
   └──────────┬───────────┘                       └───────────┬───────────┘
              │                                               │
   ┌──────────▼───────────┐                       ┌───────────▼───────────┐
   │ Vanilla JS Frontend  │                       │ JWT Auth Dependency   │
   │ (DOMPurify, Marked)  │                       │ (get_current_user)    │
   └──────────┬───────────┘                       └───────────┬───────────┘
              │                                               │
              └───────────────────────┬───────────────────────┘
                                      │
                          ┌───────────▼───────────┐
                          │   SQLite Database     │
                          │   (SQLAlchemy ORM)    │
                          └───────────────────────┘
```

---

## 🔒 Manual JWT Implementation Detail

JWTs are generated manually by constructing the header and payload, Base64URL encoding each component, computing the HMAC-SHA256 signature using Python's standard libraries (`hmac` and `hashlib`), and concatenating the three sections into a JWT.

1. **Password Hashing**: `passlib.context.CryptContext` with `bcrypt` hashes user passwords upon signup.
2. **Manual Token Generation (`Token.py`)**:
   - **Header**: `{"alg": "HS256", "typ": "JWT"}` encoded with Base64URL.
   - **Payload**: `{"user_id": id, "sub": mail, "iat": timestamp, "exp": timestamp}` encoded with Base64URL.
   - **Signature**: `hmac.new(SECRET_KEY, f"{header}.{payload}", hashlib.sha256)` encoded with Base64URL.
   - **Result**: `f"{header}.{payload}.{signature}"`.
3. **Dependency Guard (`JWT_manual_auth_depends.py` / `JWT_manul_auth_utils.py`)**:
   - Parses `HTTPBearer` credentials header (`Bearer <token>`).
   - Recomputes HMAC signature and verifies token against `SECRET_KEY`.
   - Validates expiration claim (`exp`).
   - Extracts subject claim (`sub` -> user email) and injects it into controller parameters.

---

## 🔑 API Reference

### 1. Public Authentication Endpoints
| Method | Endpoint | Description | Request Body |
| :--- | :--- | :--- | :--- |
| `POST` | `/signup` | Register a new user | `{"username": "string", "mail": "user@example.com", "password": "string"}` |
| `POST` | `/login` | Authenticate user & return JWT token | `{"mail": "user@example.com", "password": "string"}` |

### 2. Secured Notes & Account Endpoints
*All secured endpoints require header `Authorization: Bearer <access_token>`.*

| Method | Endpoint | Description | Request Body / Params |
| :--- | :--- | :--- | :--- |
| `GET` | `/get_user_notes` | Fetch all notes owned by authenticated user | None |
| `POST` | `/writeNote` | Create or update a note | `{"title": "string", "content": "string"}` |
| `DELETE` | `/deleteNote` | Delete a note by title | `{"title": "string"}` |
| `DELETE` | `/delete` | Permanently delete account and all notes | `{"password": "string"}` |

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory (optional, defaults provided):

```env
SECRET_KEY=your_super_secret_jwt_key_here
ALGORITH=HS256
CORS_ORIGINS=*
```

---

## 🚀 Installation & Local Development

Follow these simple steps to set up and run the application locally on your laptop:

### 1. Clone the Repository & Navigate
Open your terminal or command prompt and clone the repository:
```bash
git clone https://github.com/Yogendra2804/Manual-JWT-Notes-App.git
cd Manual-JWT-Notes-App
```

### 2. Create & Activate a Virtual Environment
- **On Windows**:
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```
- **On macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the Application
Run the uvicorn development server:
```bash
python -m uvicorn main:app --port 8000 --reload
```

- Open your browser and navigate to: **[http://localhost:8000](http://localhost:8000)**
- Interactive API Documentation (Swagger): **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 🌐 Production Deployment Guide

### Deploying on Render / Railway / Fly.io / AWS

1. Set start command:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
2. Set Environment Variables:
   - `CORS_ORIGINS`: Set to your production domain or `*`
   - `SECRET_KEY`: Set to a strong random 256-bit string
3. The backend automatically serves `index.html` at `/`. No separate frontend build or static web server setup is required!

---

## 📁 Project Folder Structure

```
Manual-JWT-Notes-App/
│
├── database/
│   └── database1.db              # Local SQLite database
│
├── Logs/
│   └── zlogger.py                # Logging configuration
│
├── BaseEncode64_CHATGPT.py       # Helper utilities
├── JWT_manual_auth_depends.py    # Custom dependency injection for user auth
├── JWT_manual_schema.py          # Pydantic validation schemas
├── JWT_manul_auth_utils.py       # Hashing checks & database helpers
├── JWTmodels.py                  # SQLAlchemy User & UserNotes entities
├── Token.py                      # Manual JWT generation module
├── database_config.py            # SQLite connection settings
├── engine.py                     # SQLAlchemy session engine
├── index.html                    # Glassmorphism Single Page Application
├── main.py                       # FastAPI entry point & API endpoints
├── requirements.txt              # Project Python dependencies
└── README.md                     # Documentation
```

---

## 👨‍💻 Portfolio Credits & Standards

Designed & developed to demonstrate mastery in:
- **Backend Architecture**: FastAPI, SQLAlchemy ORM, SQLite, Dependency Injection.
- **Cryptography**: Manual HMAC SHA-256 JWT Token signature creation and validation.
- **Frontend Security**: XSS prevention using `DOMPurify`, scoped `sessionStorage`, input sanitization.
- **Modern Web Design**: Glassmorphism, HSL color tokens, responsive CSS grid/flexbox, accessibility (ARIA).
