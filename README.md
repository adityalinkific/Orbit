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
APP_VERSION=1.0.0
APP_ENV=development
APP_DEBUG=true

DATABASE_URL=""

JWT_SECRET_KEY=your_jwt_secret=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=10080

LOGIN_RATE_LIMIT_MAX_REQUESTS=
LOGIN_RATE_LIMIT_WINDOW_SECONDS=
LOGIN_RATE_LIMIT_BLOCK_SECONDS=




RUN APPLICATION:-
uvicorn app.main:app --reload


For Alembic Migration:-

alembic init alembic



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
