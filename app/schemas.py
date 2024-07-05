from pydantic import BaseModel
from typing import Optional
# This class creates a schema. When you pass an object of this class to a get method, 
# data fields of that object must be provided in the specified type.
class Post(BaseModel):
    title: str
    content: Optional[str] = None # Makes the content optional. If it is not provided, it is null by default.
    id: int