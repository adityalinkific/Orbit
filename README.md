PROJECT NAME: ORBIT GOVERNANCE SYSTEM API

The Orbit Governance System is a role-based task, project, and document management platform designed for
enterprise governance


PROJECT STRUCTURE: -

TaskFlow/
│
├── app/
│   │
│   ├── core/
│   │   ├── dependency.py
│   │   ├── security.py
│   │   ├── config.py
│   │   ├── middleware/
│   │   └── database
│   │       └── database.py
│   │
│   ├── modules/
│   │   └── auth/
│   │       ├── auth_controller.py
│   │       ├── auth_model.py
│   │       ├── auth_repository.py
│   │       ├── auth_routes.py
│   │       └── auth_schema.py
│   │
│   └── main.py
│
├── .env
├── requirements.txt
└── README.md


FEATURES: -

- Modular folder structure
- JWT-based authentication


TECH STACK:-

Backend        : Python (FastAPI)
Database       : PostgreSQL
Authentication : JWT
ORM            : SQLAlchemy (Async)
API Testing    : Swagger UI and Postman


INSTALLATION:-

1. Clone Repository

git clone <repository-url>
cd orbit


2. Install Dependencies

python -m venv venv
source venv/bin/activate   (Linux/Mac)
venv\Scripts\activate      (Windows)
pip install -r requirements.txt

ENVIRONMENT VARIABLES: -

Create a `.env` file in the root directory.

APP_NAME=Orbit
APP_ENV=development
APP_DEBUG=true

DB_HOST=mysql
DB_PORT=3306
DB_NAME=orbit
DB_USER=root
DB_PASSWORD=root

JWT_SECRET_KEY=your_jwt_secret
JWT_EXPIRE_MINUTES=10080

RUN APPLICATION:-

uvicorn app.main:app --reload


ERROR HANDLING:-

Centralized error-handling middleware handles:
401 - Unauthorized
403 - Forbidden
404 - Not Found
422 - Validation Error
500 - Internal Server Error


API DOCUMENTATION:-

Swagger UI available at:
http://localhost:8000/docs
