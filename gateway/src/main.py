from fastapi import FastAPI
from gateway.src.apps.documents.router import router as documents_router
import uvicorn

app = FastAPI()
app.include_router(documents_router)


@app.get("/healthcheck")
async def healthcheck():
    return True


if __name__ == "__main__":
    uvicorn.run(app)
