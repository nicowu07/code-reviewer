from fastapi import FastAPI, Request, Form, Depends
from app.database.connection import Base, data_engine
from app.routers import review, results
from app.exceptions import global_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError

import tempfile


app = FastAPI()
Base.metadata.create_all(bind=data_engine)

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(review.router)
app.include_router(results.router)


