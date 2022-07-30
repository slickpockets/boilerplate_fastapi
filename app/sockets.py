from config import sio

@sio.on('client_connect_event')
async def handle_client_connect_event(sid, *args, **kwargs):
    mqtt.publish("/mqtt", "Hello from Fastapi")
    #app.sio.emit('testy2', {'data': 'connection was successful'})

@sio.on('client_start_event')
async def handle_client_start_event(sid, *args, **kwargs): # (!)
    print('Server says: start_event worked')
    await app.sio.emit('testy',{'data':'start event worked'})
