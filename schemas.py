from pydantic import BaseModel, HttpUrl


class SourceSchema(BaseModel):
    title: str
    url: HttpUrl
    xpath: str
