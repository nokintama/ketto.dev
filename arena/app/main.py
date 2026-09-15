from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from app.ws.protocol import Envelope, QueueJoin, ChatSend
from json import JSONDecodeError


app = FastAPI()


def error(code: str, message: str) -> dict:
    return {"type": "error", "data": {"code": code, "message": message}}


@app.get("/status")
async def status():
    return {"status": "ok"}


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()

    try:
        while True:
            try:
                message = await ws.receive_json()
            except JSONDecodeError:
                await ws.send_json(error("invalid_message", "Not a JSON"))
                continue

            try:
                envelope = Envelope.model_validate(message)
            except ValidationError:
                await ws.send_json(error("invalid_message", "Bad envelope"))
                continue

            if envelope.type == "queue.join":
                try:
                    payload = QueueJoin.model_validate(envelope.data)
                except ValidationError:
                    await ws.send_json(
                        error("invalid_payload", "Bad queue.join payload")
                    )
                    continue
                print("в очередь:", payload.language)

            elif envelope.type == "chat.send":
                try:
                    payload = ChatSend.model_validate(envelope.data)
                except ValidationError:
                    await ws.send_json(
                        error("invalid_payload", "Bad chat.send payload")
                    )
                    continue
                print("chat:", payload.text)

            else:
                await ws.send_json(
                    error("unknown_type", f"Unknown type: {envelope.type}")
                )

    except WebSocketDisconnect:
        print("client disconected")
