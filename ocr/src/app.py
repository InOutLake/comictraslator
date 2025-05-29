from fastapi import FastAPI
import pika
import uvicorn

app = FastAPI()
connection = pika.BlockingConnection(...)
channel = connection.channel


@app.get("/")
def home():
    return "What's up fella!"


@app.get("/healthcheck")
def readiness():
    return True


if __name__ == "__main__":
    uvicorn.run(app)
