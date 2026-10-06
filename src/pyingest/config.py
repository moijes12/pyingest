from typing import Literal

from pydantic import BaseModel


class CsvSourceConfig(BaseModel):
    type: Literal["csv"]


class ApiSourceConfig(BaseModel):
    type: Literal["api"]
