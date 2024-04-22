import json

from sanic import Request, Websocket


async def handler(request: Request, ws: Websocket, chat_id: str):
    await ws.send(json.dumps({"chat_id": chat_id, "message": "Welcome"}))

    async for msg in ws:
        await ws.send(json.dumps(
            {
                "echo": msg,
                "chat_id": chat_id
            }
        ))
