from fastapi import FastAPI

# Create FastAPI instance
app = FastAPI(
    title="Iktomi API",
    description="This is a simple FastAPI application.",
    version="0.0.1",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)


# Root endpoint
@app.get("/api/")
def read_root():
    return {"message": "Welcome to my FastAPI app!"}
