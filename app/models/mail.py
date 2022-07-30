from pydantic import EmailStr, BaseModel
from typing import List, Dict, Any

class EmailSchema(BaseModel):
    email: List[EmailStr]
