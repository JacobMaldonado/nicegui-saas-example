from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    id: str
    email: str
    created_at: str = datetime.now().isoformat()
    plan: str = "free"
    credits: int = 5
