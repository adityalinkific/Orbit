PROJECT NAME: ORBIT GOVERNANCE SYSTEM API

The Orbit Governance System is a role-based task, project, and document management platform designed for
enterprise governance


PROJECT STRUCTURE: -

TaskFlow/
│
├── app/
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── dependency.py
│   │   ├── schema.py
│   │   ├── security.py
│   │   ├── database/
│   │   │   └── database.py
│   │   └── middleware/
│   │       ├── error_handlers.py
│   │       └── cors_middleware.py
│   │
│   ├── modules/
│   │
│   ├── modules/
│   │   ├── auth/
│   │   │   ├── auth_model.py
│   │   │   ├── auth_repository.py
│   │   │   ├── auth_routers.py
│   │   │   ├── auth_schema.py
│   │   │   └── auth_services.py
│   │   │
│   │   ├── department/
│   │   │   ├── department_controller.py
│   │   │   ├── department_model.py
│   │   │   ├── department_repository.py
│   │   │   ├── department_routers.py
│   │   │   ├── department_schema.py
│   │   │   └── department_services.py
│   │   │
│   │   ├── health/
│   │   │   ├── health_controller.py
│   │   │   ├── health_repository.py
│   │   │   ├── health_routers.py
│   │   │   └── health_services.py
│   │   │
│   │   ├── project/
│   │   │   ├── project_controller.py
│   │   │   ├── project_model.py
│   │   │   ├── project_repository.py
│   │   │   ├── project_routers.py
│   │   │   ├── project_schema.py
│   │   │   └── project_services.py
│   │   │
│   │   ├── role/
│   │   │   ├── role_controller.py
│   │   │   ├── role_repository.py
│   │   │   ├── role_routers.py
│   │   │   ├── role_schema.py
│   │   │   └── role_services.py
│   │   │
│   │   ├── task/
│   │   │   ├── task_controller.py
│   │   │   ├── task_model.py
│   │   │   ├── task_repository.py
│   │   │   ├── task_routers.py
│   │   │   ├── task_schema.py
│   │   │   └── task_services.py
│   │   │
│   │   └── user/
│   │       ├── user_controller.py
│   │       ├── user_repository.py
│   │       ├── user_routers.py
│   │       ├── user_schema.py
│   │       └── user_services.py
│   │
│   ├── routers/
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

1. Clone Repository:-

git clone <repository-url>
cd orbit


2. Install Dependencies:-

python -m venv venv
source venv/bin/activate   (Linux/Mac)
venv\Scripts\activate      (Windows)
pip install -r requirements.txt

3. ENVIRONMENT VARIABLES:-

Create a `.env` file in the root directory.

APP_NAME=Orbit
APP_VERSION=1.0.0
APP_ENV=development
APP_DEBUG=true
FRONTEND_URL='["http://localhost:5173","http://localhost:3000"]'

DATABASE_URL=""

JWT_SECRET_KEY=your_jwt_secret=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=10080

LOGIN_RATE_LIMIT_MAX_REQUESTS=
LOGIN_RATE_LIMIT_WINDOW_SECONDS=
LOGIN_RATE_LIMIT_BLOCK_SECONDS=




4. RUN APPLICATION:-
uvicorn app.main:app


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
or
domain-url/docs
