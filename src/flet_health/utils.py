from datetime import datetime
from enum import Enum
from typing import Any, Optional


def wrap_param(
    param_value: Any,
    type_name: Optional[str] = None,
    subtype_name: Optional[str] = None,
    class_name: Optional[str] = None,
) -> dict:
    """
    Packs a parameter to be sent to Flutter with standardized metadata.

    If `type_name` is not entered, it will be inferred automatically based on `param_value`.
    """

    if type_name is None:
        match param_value:
            case None:
                type_name = None
            case bool():
                type_name = "bool"
            case int():
                type_name = "int"
            case float():
                type_name = "float"
            case str():
                type_name = "str"
            case list():
                type_name = "list"
                if param_value and isinstance(param_value[0], Enum):
                    subtype_name = "enum"
                    class_name = param_value[0].__class__.__name__
                    param_value = [enum.value for enum in param_value] if param_value else []
            case dict():
                type_name = "dict"
            case Enum():
                type_name = "enum"
                class_name = param_value.__class__.__name__
                param_value = param_value.value
            case datetime():
                type_name = "date"
                param_value = int(param_value.timestamp() * 1000)
            case _:
                type_name = "unknown"
                # raise TypeError(
                #     f"Unsupported type {type(param_value)} for value {param_value}"
                # )

    if type_name != "enum" and isinstance(param_value, Enum):
        type_name = "enum"
        class_name = param_value.__class__.__name__
        param_value = param_value.value

    return {
        "value": param_value,
        "type": type_name,
        "subtype": subtype_name,
        "class_name": class_name,
    }
