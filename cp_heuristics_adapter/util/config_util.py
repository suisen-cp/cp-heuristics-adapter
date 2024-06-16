from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class ConfigKey(Generic[T]):
    """Key for loading a configuration value.

    Attributes:
        key (str): Key in the configuration file.
        default (T): Default value.
    """

    key: str
    default: T

    def load_from(self, config: dict[str, T]) -> T:
        """Load the value from the config.

        Args:
            config (dict[str, T]): Configuration.
        Returns:
            T: Value from the configuration.
        """
        return config.get(self.key, self.default)
