from sanic import text


async def handler(request):
    return text("Hello, world")
