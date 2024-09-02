from pydantic import BaseModel

# Pydantic model for the request body
class UserRequest(BaseModel):
    question: str
    tag: str
    chat_id: str