from fastapi import FastAPI
import uvicorn

from routers import routers
from config import config
from database import Base, engine
from database.models import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url=config.DOCS_ROUTE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Update with your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    app.include_router(router.router, prefix=router.prefix, tags=router.tags)


def main():
    Base.metadata.create_all(engine)
    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=True)


if __name__ == '__main__':
    main()
