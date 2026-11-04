from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator

class JobCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=10)
    location: str | None = Field(default=None, max_length=100)
    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def check_salary_range(self):
        if(
            self.salary_min is not None
        )