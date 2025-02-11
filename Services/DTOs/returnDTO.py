from pydantic import BaseModel

class ReturnDTO(BaseModel):

    """
    ReturnDTO is a data transfer object that is used to return data from services to controllers.
    It contains the following attributes:
    - status: bool, denoting whether the operation was successful or not
    - message: str, containing the message for the operation
    - data: any, containing the data returned from the operation, None if failed / no data
    """

    status: bool = False
    message: str = ""
    data: any = None

    class Config:
        arbitrary_types_allowed = True