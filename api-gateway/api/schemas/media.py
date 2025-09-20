from pydantic import BaseModel


class FileUploadResponseS(BaseModel):
    id: str
    url: str

class GetFileUrlResponse(BaseModel):
    url: str