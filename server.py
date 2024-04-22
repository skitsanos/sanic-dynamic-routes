import logging
import socket

from sanic import Sanic, Request

from utils.router import load_routes

hostname = socket.gethostname()
logging.basicConfig(
    level=logging.DEBUG,  # Set the desired logging level
    format=f'%(asctime)s [%(levelname)s] {hostname} %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

app = Sanic("MyHelloWorldApp")


@app.on_request
async def check_token(request: Request):
    logging.debug(request.token)


@app.on_response
async def custom_banner(request, response):
    response.headers["server"] = "sanic-api-server"


# @app.get("/")
# async def hello_world(request):
#     return text("Hello, world.")

load_routes(app, "routes")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, auto_reload=True)
