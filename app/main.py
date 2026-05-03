from fastapi import FastAPI
from app.database.connection import Base, data_engine
from app.routers import review, results, dashboard
from app.exceptions import global_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError



app = FastAPI()
Base.metadata.create_all(bind=data_engine)

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(review.router)
app.include_router(results.router)
app.include_router(dashboard.router)


