import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db_models import Base
from database import engine
from routers import users

description = """
Example API to demonstrate SSO logins with FastAPI
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title='FastAPI SSO with providers example',
    description=description,
    version="1.0.0",
    docs_url="/v1/documentation",
    redoc_url="/v1/redocs",
    lifespan=lifespan
)

app.include_router(users.router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9999)
