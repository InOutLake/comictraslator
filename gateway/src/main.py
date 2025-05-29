from fastapi import FastAPI
import pika
import uvicorn

app = FastAPI()
connection = pika.BlockingConnection()


@app.get("/healthcheck")
async def healthcheck():
    return True


if __name__ == "__main__":
    uvicorn.run(app)
