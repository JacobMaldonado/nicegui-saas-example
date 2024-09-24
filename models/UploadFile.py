from pydantic import BaseModel

class UploadFile(BaseModel):
    file: bytes
    file_name: str
    type: str