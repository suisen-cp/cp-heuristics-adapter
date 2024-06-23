from typing import Any
import pytest

from cp_heuristics_adapter.util.config_util import ConfigKey


class TestConfigKey:
    @pytest.fixture
    def config(self) -> dict[str, Any]:
        return {
            "int_val": 1,
            "str_val": "value",
            "list_val": ["a", "b"],
        }

    @pytest.mark.parametrize(
        "config_key, expected",
        [
            (ConfigKey[int]("int_val", 0), 1),
            (ConfigKey[str]("str_val", "default"), "value"),
            (
                ConfigKey[list[str]](
                    "list_val", ["this", "is", "a", "default", "list"]
                ),
                ["a", "b"],
            ),
        ],
    )
    def test_load_existing_entry(
        self, config: dict[str, Any], config_key: ConfigKey[Any], expected: Any
    ) -> None:
        assert config_key.load_from(config) == expected

    @pytest.mark.parametrize(
        "config_key, expected",
        [
            (ConfigKey[int]("int_val_", 0), 0),
            (ConfigKey[str]("str_val_", "default"), "default"),
            (
                ConfigKey[list[str]](
                    "list_val_", ["this", "is", "a", "default", "list"]
                ),
                ["this", "is", "a", "default", "list"],
            ),
        ],
    )
    def test_load_non_existing_entry(
        self, config: dict[str, Any], config_key: ConfigKey[Any], expected: Any
    ) -> None:
        assert config_key.load_from(config) == expected
