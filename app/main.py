from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi import BackgroundTasks
from starlette.responses import JSONResponse
from starlette.responses import HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# from typing import List, Dict

from .cache import cache
from .entities import load_cheapest_routes


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await cache.startup()


@app.on_event("shutdown")
async def shutdown_even():
    await cache.close()


@app.exception_handler(StarletteHTTPException)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(
            {"detail": exc.detail, "status_code": exc.status_code}
        ),
    )


@app.get("/", response_class=HTMLResponse)
def index(background_tasks: BackgroundTasks):
    # background_tasks(load_cheapest_routes())

    _html = """
     <html>
        <head><title>Aviata Inteview Task</title></head>
        <body>
          <br>
          <center>
            Please refer to the
            <a href="/docs">documentation</a> for guidance.<br>
            To see the cheapest price routes
            <a href="/best/offers/">click here</a>
          </center>
        </body>
      </html>
    """

    # ss = load_cheapest_routes()
    return _html


@app.get("/best/offers/")
def get_hot_routes():
    routes = load_cheapest_routes()
    return routes
