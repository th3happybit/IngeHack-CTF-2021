import uvicorn
import time
from fastapi import FastAPI, Form
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.errors.http_error import http_error_handler
from api.errors.validation_error import http422_error_handler
from core.config import (
        ALLOWED_HOSTS,
        API_PREFIX,
        DEBUG,
        PROJECT_NAME,
        VERSION,
        UVICORN_HOST,
        UVICORN_PORT,
        UVICORN_RELOAD,
        UVICORN_ACCESS_LOG,
        UVICORN_LOG_LEVEL,
    )
from core.redis.storage import RedisStorage

def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    # Middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_application()
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="templates")
r = RedisStorage()

@app.middleware("http")
async def CSPMiddleware(request: Request, call_next):
    response = await call_next(request)
    # response.headers[
    #     "Content-Security-Policy"
    # ] = "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline';"
    return response


@app.get("/", response_class=HTMLResponse)
async def valhala(request: Request):
    return templates.TemplateResponse("valhala.html", {"request": request})

@app.get("/report", response_class=HTMLResponse)
async def report(request: Request):
    return templates.TemplateResponse("report.html", {"request": request})

@app.post("/do_report")
async def do_report_handler(request: Request,url: str = Form(...)):
    current_time = time.time()
    ip = str(request.client.host)
    last_time = r.getValue('time.'+ip)
    last_time = float(last_time) if last_time is not None else 0
    
    time_diff = current_time - last_time

    if time_diff > 6:
        r.rpush('submissions', url)
        r.setEx('time.'+ip, 60, current_time)
        return "submitted"

    return "rate limited"
    

if __name__ == "__main__":
    uvicorn.run("main:app", port=UVICORN_PORT, host=UVICORN_HOST, reload=UVICORN_RELOAD, access_log=UVICORN_ACCESS_LOG, log_level=UVICORN_LOG_LEVEL)
