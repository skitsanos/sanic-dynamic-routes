from sanic import json


async def handler(request, user_id: str):
    return json({
        "user": user_id
    })
