
from app.api.v1 import *
from fastapi import FastAPI
from app.exceptions.handler import *


app = FastAPI()
app.include_router(v1_router, prefix="/v1")

app.add_exception_handler(AppBaseException, app_base_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)