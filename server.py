from sanic import Sanic
from sanic.response import text

from utils.router import load_routes

app = Sanic("MyHelloWorldApp")


@app.on_response
async def custom_banner(request, response):
    response.headers["server"] = "sanic-api-server"


# @app.get("/")
# async def hello_world(request):
#     return text("Hello, world.")

load_routes(app, "routes")
