import uvicorn

from fastapi import FastAPI
from starlette.responses import RedirectResponse
from controllers import catalog
from settings import Settings

settings = Settings()

app = FastAPI(
    title="HC-Catalog API",
    description="API to retrieve catalogs",
    version="1.0.1",
    root_path=settings.ROOT_PATH,
    redoc_url=None,
)

app.include_router(catalog.router)

@app.get("/", include_in_schema=False)
async def root():
    return {"Hello": "HC-Catalog API"}


@app.get("/hc-catalog/openapi.json", include_in_schema=False)
async def root():
    return RedirectResponse("/openapi.json")


# USE ONLY IN LOCAL DEVELOPMENT
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1000)
