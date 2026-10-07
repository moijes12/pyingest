import pytest
from pydantic import ValidationError

from pyingest.config import ApiSourceConfig, CsvSourceConfig, PostgresSinkConfig


def test_CsvSourceConfig_creation() -> None:
    k = CsvSourceConfig(type="csv")
    assert type(k) is CsvSourceConfig


def test_CsvSourceConfig_incorrect_type() -> None:
    with pytest.raises(ValueError):
        CsvSourceConfig(type="json")


def test_ApiSourceConfig_creation() -> None:
    k = ApiSourceConfig(type="api")
    assert type(k) is ApiSourceConfig


def test_ApiSourceConfig_incorrect_type() -> None:
    with pytest.raises(ValueError):
        ApiSourceConfig(type="json")


def test_PostgresSinkConfig_creation() -> None:
    for strategy in ["append_only", "upsert", "ignore"]:
        k = PostgresSinkConfig(
            type="postgres",
            dsn_env="PYINGEST_PG_DSN",
            schema="public",
            table="orders",
            conflict_strategy=strategy,
        )
        assert type(k) is PostgresSinkConfig
        # Validate that schema_name is correctly populated through the alias
        assert k.schema_name == "public"


def test_PostgresSinkConfig_creation_default_strategy() -> None:
    k = PostgresSinkConfig(
        type="postgres",
        dsn_env="PYINGEST_PG_DSN",
        schema="public",
        table="orders",
    )
    assert type(k) is PostgresSinkConfig
    # Validate that the default strategy is set to upsert
    assert k.conflict_strategy == "upsert"


def test_PostgresSinkConfig_creation_invalid_table() -> None:
    with pytest.raises(ValueError):
        PostgresSinkConfig(
            type="postgres",
            dsn_env="PYINGEST_PG_DSN",
            schema="public",
            table="public:orders",
        )


def test_PostgresSinkConfig_creation_invalid_conflict_strategy() -> None:
    with pytest.raises(ValidationError) as exc_info:
        PostgresSinkConfig(
            type="postgres",
            dsn_env="PYINGEST_PG_DSN",
            schema="public",
            table="orders",
            conflict_strategy="foo",
        )
    errors = exc_info.value.errors()
    conflict_strategy_error = next(
        (err for err in errors if "conflict_strategy" in err["loc"]), None
    )

    assert conflict_strategy_error is not None
    assert conflict_strategy_error["type"] == "literal_error"
    assert conflict_strategy_error["input"] == "foo"
