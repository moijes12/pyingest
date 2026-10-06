import pytest

from pyingest.config import ApiSourceConfig, CsvSourceConfig


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
