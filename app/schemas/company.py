from pydantic import BaseModel, ConfigDict, Field

class CompanyCreate(BaseModel):
    name: str = Field(min_length=4, max_length=150)
    description: str | None = None
    location: str | None = Field(default=None, max_length=100)


class CompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    location: str | None
    owner_id: int