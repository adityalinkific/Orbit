from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from app.routers import api_router
import app.models
from app.core.middleware.error_handlers import http_exception_handler, response_validation_exception_handler, global_exception_handler, custom_request_validation_exception_handler
from app.core.middleware.cors_middleware import register_cors
from app.core.config import settings

app = FastAPI(
        title= settings.APP_NAME,
        version= settings.APP_VERSION,
        description="Backend Management System",
        contact={
            "name": "API Support",
            "url": "mailto:support@orbit.dev",
        },
        license_info={
            "name": "Proprietary- Internal Use Only",
            'url': "https://demo.com"
        },
    )

register_cors(app)

app.add_exception_handler(RequestValidationError, custom_request_validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(ResponseValidationError, response_validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(api_router)

@app.get("/")
def root():
    return {
        "status" : True,
        "message" : "Orbit API Running Successfully!"
    }
