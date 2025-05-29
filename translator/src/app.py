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
    queue = channel.queue_declare(queue="readiness", exclusive=True)
    channel.exchange_declare(exchange="readiness", exchange_type="direct")
    channel.bind(exchange="readiness", queue=queue.methods.queue)


if __name__ == "__main__":
    uvicorn.run(app)
