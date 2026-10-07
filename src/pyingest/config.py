from typing import Literal

from pydantic import BaseModel, Field

_SINK_REGEX_VALIDATOR = r"^[a-zA-Z_][a-zA-Z0-9_]*$"


class CsvSourceConfig(BaseModel):
    type: Literal["csv"]


class ApiSourceConfig(BaseModel):
    type: Literal["api"]


class PostgresSinkConfig(BaseModel):
    type: Literal["postgres"]
    dsn_env: Literal["PYINGEST_PG_DSN"] = "PYINGEST_PG_DSN"
    schema_name: str = Field(alias="schema", pattern=_SINK_REGEX_VALIDATOR)
    table: str = Field(pattern=_SINK_REGEX_VALIDATOR)
    conflict_strategy: Literal["upsert", "append_only", "ignore"] = "upsert"
