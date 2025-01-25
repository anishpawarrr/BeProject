from pydantic import BaseModel

class ReturnDTO(BaseModel):
    status: bool = False
    message: str = ""
    data: any = None

    class Config:
        arbitrary_types_allowed = True