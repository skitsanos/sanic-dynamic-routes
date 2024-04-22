from sanic import json, Request


async def handler(request:Request):
    return json({
        "version": "1.0.0",
        "headers": [h for h in request.headers],
    })
