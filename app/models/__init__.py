# from app.modules.auth.auth_model import User, Role
# from app.modules.department.department_model import Department
# from app.modules.project.project_model import Project

# """
# Automatic model discovery for Alembic.

# Imports all *_model.py files inside app/modules/*
# """

import importlib
import pkgutil
from app import modules

for _, module_name, _ in pkgutil.iter_modules(modules.__path__):
    try:
        importlib.import_module(f"app.modules.{module_name}.{module_name}_model")
    except ModuleNotFoundError:
        # module has no model file → ignore
        pass

# from app.modules.auth.auth_model import User, Role