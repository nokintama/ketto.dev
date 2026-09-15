from pydantic import BaseModel


class Envelope(BaseModel):
    type: str
    data: dict


class QueueJoin(BaseModel):
    user_id: int
    language: str


class ChatSend(BaseModel):
    text: str
