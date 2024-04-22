from sanic import json

protected = True


async def handler(request, user_id: str):
    return json({
        "user": user_id
    })
