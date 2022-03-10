from typing import Optional

from fastapi import FastAPI
from fastapi_socketio import SocketManager
app = FastAPI()
sio = SocketManager(app=app)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@sio.on("test")
async def handle_test(sid, *args, **kwargs):
    await sio.emit("hi")
