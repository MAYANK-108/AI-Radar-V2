from pydantic import BaseModel,ConfigDict
from datetime import datetime
from typing import Optional 

class ArticleResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id : int
    title : str
    url : str
    source : Optional[str] = None
    summary : Optional[str] = None
    score : Optional[int] = None
    discovered_at : datetime