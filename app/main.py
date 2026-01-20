from fastapi import FastAPI
from app.routers import api_router

app = FastAPI(
        title= "TaskFlow API",
        version= "1.0.0",
        description="Task Management System For Intern",
        contact={
            "name": "API Support",
            "url": "mailto:support@orbit.dev",
        },
        license_info={
            "name": "Proprietary- Internal Use Only",
            'url': 'http://localhost:8000/'
        },
    )

app.include_router(api_router)
