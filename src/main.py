import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router as api_router
from core.config import app_config

app = FastAPI(
    title="Reddit3000",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router.router)


def main():
    uvicorn.run(
        app="main:app",
        host=app_config.HOST,
        port=app_config.PORT,
        reload=app_config.ENV == "local",
        workers=1,
    )


if __name__ == "__main__":
    main()
