"""
Base model utilities for Asana simulation entities.

Provides lightweight dataclass helpers to standardize
dictionary conversion and instance creation across generators.
"""

from dataclasses import dataclass, asdict
from typing import Any, Dict, Type, TypeVar


T = TypeVar("T", bound="BaseModel")


@dataclass
class BaseModel:
    """
    Common parent class for all generated data entities.
    """

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert dataclass instance to a dictionary.

        Returns:
            Dictionary representation of the dataclass.
        """
        return asdict(self)

    def __repr__(self) -> str:
        """
        Return a readable string representation.

        Returns:
            String representation with field values.
        """
        attrs = ", ".join(f"{key}={value!r}" for key, value in asdict(self).items())
        return f"<{self.__class__.__name__}({attrs})>"


class FactoryMixin:
    """
    Mixin providing factory construction from dictionaries.
    """

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Create a dataclass instance from a dictionary.

        Args:
            data: Field-value mapping.

        Returns:
            Instantiated dataclass object.
        """
        obj = cls(**data)
        return obj


__all__ = ["BaseModel", "FactoryMixin"]


if __name__ == "__main__":
    from dataclasses import dataclass

    @dataclass
    class DummyModel(BaseModel, FactoryMixin):
        id: str
        name: str
        active: bool = True

    obj = DummyModel.from_dict({"id": "demo_1", "name": "Test Entity", "active": False})

    print("[✅] BaseModel and FactoryMixin working correctly.")
    print(obj)
    print(obj.to_dict())
