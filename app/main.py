from typing import Optional

from fastapi import FastAPI, Request
from fastapi_socketio import SocketManager
from fastapi_mqtt import FastMQTT, MQQTConfig
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.applications import Starlette
from pathlib import Path
app = FastAPI()
mqtt_config = MQQTConfig()
mqtt = FastMQTT(
    config=mqtt_config
)

sio = SocketManager(app=app)
mqtt.init_app(app)
path = Path.cwd()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

mqtt_topics = {"/mqtt": "hello"}


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/mqtt") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    print(topic, payload.decode())
    await app.sio.emit("test", payload.decode())
    return 0

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/item", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("item.html", {"request": request})

@app.sio.on("test")
async def handle_test(sid, *args, **kwargs):
    print("test")
    return 0

@app.sio.on("test2")
async def handle_test(sid, *args, **kwargs):
    print("test2")
    mqtt.publish("/test2", "yo")
    return 0



@app.sio.on('client_connect_event')
async def handle_client_connect_event(sid, *args, **kwargs):
    mqtt.publish("/mqtt", "Hello from Fastapi")
    #app.sio.emit('testy2', {'data': 'connection was successful'})

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
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True, debug=True  )
