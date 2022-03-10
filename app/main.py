from typing import Optional

from fastapi import FastAPI
from fastapi_socketio import SocketManager
from fastapi_mqtt import FastMQTT, MQQTConfig
from fastapi.staticfiles import StaticFiles

app = FastAPI()
mqtt_config = MQQTConfig()
mqtt = FastMQTT(
    config=mqtt_config
)

sio = SocketManager(app=app)
mqtt.init_app(app)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/mqtt") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    return 0

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


@app.get("/")
async def func():
    mqtt.publish("/mqtt", "Hello from Fastapi") #publishing mqtt topic
    return {"result": True,"message":"Published" }


@sio.on("test")
async def handle_test(sid, *args, **kwargs):
    await sio.emit("hi")

if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG,
                        stream=sys.stdout)
    import uvicorn
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True, debug=False)
