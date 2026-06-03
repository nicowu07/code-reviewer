from fastapi import FastAPI
from app.database.connection import Base, data_engine
from app.routers import review, results, dashboard
from app.exceptions import global_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError
from app.config import limiter
from app.config import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from app.config import templates



app = FastAPI()
Base.metadata.create_all(bind=data_engine)

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(review.router)
app.include_router(results.router)
app.include_router(dashboard.router)

async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return templates.TemplateResponse(
        request=request,
        name='error.html',
        context={"message": f"Rate limit exceeded. Please wait a minute before trying again."},
        status_code=429
    )

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


