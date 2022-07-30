from fastapi.responses import HTMLResponse
from config import templates, app, conf
from fastapi import Request, BackgroundTasks
from models.mail import EmailSchema
from fastapi_mail import FastMail, MessageSchema
from starlette.responses import JSONResponse

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("default/index.html", {"request": request})

@app.post("/emailbackground")
async def send_in_background(
    background_tasks: BackgroundTasks,
    email: EmailSchema
    ) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=email.dict().get("email"),
        body="Simple background task",
        )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message,message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})
