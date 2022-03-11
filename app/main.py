from typing import Optional

from fastapi import FastAPI, Request
from fastapi_socketio import SocketManager
from fastapi_mqtt import FastMQTT, MQQTConfig
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.applications import Starlette

app = FastAPI()
mqtt_config = MQQTConfig()
mqtt = FastMQTT(
    config=mqtt_config
)

sio = SocketManager(app=app)
mqtt.init_app(app)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



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
async def home():
    mqtt.publish("/mqtt", "Hello from Fastapi") #publishing mqtt topic
    return {"result": True,"message":"Published" }


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})


@app.sio.on("test")
async def handle_test(sid, *args, **kwargs):
    print("hit")
    await sio.emit("hi")


@app.sio.on('client_connect_event')
async def handle_client_connect_event(sid, *args, **kwargs): # (!)
    await app.sio.emit('testy2', {'data': 'connection was successful'})

@app.sio.on('client_start_event')
async def handle_client_start_event(sid, *args, **kwargs): # (!)
    print('Server says: start_event worked')
    await app.sio.emit('testy',{'data':'start event worked'})




if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG,
                        stream=sys.stdout)
    import uvicorn
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True, debug=False)
