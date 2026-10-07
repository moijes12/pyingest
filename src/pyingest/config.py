from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

_IDENTIFIER_PATTERN = r"^[a-zA-Z_][a-zA-Z0-9_]*$"


class _StrictBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class CsvSourceConfig(_StrictBaseModel):
    type: Literal["csv"]


class ApiSourceConfig(_StrictBaseModel):
    type: Literal["api"]


class PostgresSinkConfig(_StrictBaseModel):
    type: Literal["postgres"]
    dsn_env: str = "PYINGEST_PG_DSN"
    schema_name: str = Field(alias="schema", pattern=_IDENTIFIER_PATTERN)
    table: str = Field(pattern=_IDENTIFIER_PATTERN)
    # append_only opts out of the idempotency guarantee
    conflict_strategy: Literal["upsert", "append_only", "ignore"] = "upsert"
