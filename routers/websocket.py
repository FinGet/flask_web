from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

router = APIRouter()
html = """

<!DOCTYPE html>

<html>

    <head>

        <title>Chat</title>

    </head>

    <body>

        <h1>WebSocket 聊天</h1>

        <form action="" onsubmit="sendMessage(event)">

            <input type="text" id="messageText" autocomplete="off"/>

            <button>Send</button>

        </form>

        <ul id='messages'>

        </ul>

        <script>

            var ws = new WebSocket("ws://localhost:8000/websocket/ws");

            ws.onmessage = function(event) {

                var messages = document.getElementById('messages')

                var message = document.createElement('li')

                var content = document.createTextNode(event.data)

                message.appendChild(content)

                messages.appendChild(message)

            };

            function sendMessage(event) {

                var input = document.getElementById("messageText")

                ws.send(input.value)

                input.value = ''

                event.preventDefault()

            }
</script>

    </body>

</html>

"""

@router.get('/')
async def get():
    return HTMLResponse(html)

@router.websocket("/ws") # websocket 路由
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept() # 接受连接
    while True:
        data = await websocket.receive_text() # 接收文本
        if data == "close":
            await websocket.send_text(f"Message text was: {data}")
            await websocket.send_text('聊天结束')
            await websocket.close(100)
        await websocket.send_text(f"Message text was: {data}") # 发送文本