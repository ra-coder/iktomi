from fastapi import FastAPI

from vk.login import vk_login_router

# Create FastAPI instance
app = FastAPI(
    title="Iktomi API",
    description="This is a simple FastAPI application.",
    version="0.0.1",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.include_router(vk_login_router)


# Root endpoint
@app.get("/api/")
def read_root():
    return {"message": "Welcome to my FastAPI app!"}
