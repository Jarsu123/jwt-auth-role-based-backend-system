# Scalable Notes API (Backend Intern Assignment)

A professional-grade RESTful API built with FastAPI, featuring JWT Authentication, Role-Based Access Control (RBAC), and a responsive React.js frontend.

## 🚀 Key Features

- **Authentication**: Secure registration and login with JWT and password hashing (Bcrypt).
- **Role-Based Access (RBAC)**: Distinct permissions for `Admin` and `User` roles.
- **Notes Management**: Full CRUD operations for personal notes.
- **API Documentation**: Interactive Swagger UI at `/docs`.
- **Validation**: Strict input validation using Pydantic (email validation, length constraints).
- **Logging**: Structured application logging for monitoring and debugging.
- **Containerization**: Docker and Docker Compose support for easy deployment.

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, Pydantic, PostgreSQL.
- **Frontend**: React.js, Axios, React Router.
- **Database**: PostgreSQL (Docker) / SQLite (Local).
- **Security**: JWT (JSON Web Tokens), Passlib (Bcrypt).

## 📥 Installation & Setup

### Using Docker (Recommended)
1. Ensure you have Docker and Docker Compose installed.
2. Run:
   ```bash
   docker-compose up --build
   ```
3. Backend: `http://localhost:8000` | Frontend: `http://localhost:3000`

### Local Setup
1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

## 📖 API Documentation
Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---
*Developed as a part of the Backend Developer Intern Assignment.*
