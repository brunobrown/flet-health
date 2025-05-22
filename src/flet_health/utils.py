from datetime import datetime
from enum import Enum
from typing import Optional, Any


def wrap_value(
    param_value: Any,
    type_name: Optional[str] = None,
    subtype_name: Optional[str] = None,
    class_name: Optional[str] = None
) -> dict:
    if param_value is None:
        return {
            "value": None,
            "type": type_name or "none",
            "subtype": subtype_name,
            "class_name": class_name
        }

    if type_name == "list" and isinstance(param_value, list):
        items = [v.value if isinstance(v, Enum) else v for v in param_value]
        return {
            "value": items,
            "type": "list",
            "subtype": subtype_name,
            "class_name": class_name
        }

    match param_value:
        case bool():
            return {"value": param_value, "type": "bool", "subtype": None, "class_name": None}
        case int():
            return {"value": param_value, "type": "int", "subtype": None, "class_name": None}
        case float():
            return {"value": param_value, "type": "float", "subtype": None, "class_name": None}
        case str():
            return {"value": param_value, "type": "str", "subtype": None, "class_name": None}
        case datetime():
            return {
                "value": int(param_value.timestamp() * 1000),
                "type": "date",
                "subtype": None,
                "class_name": None
            }
        case Enum():
            return {
                "value": param_value.value,
                "type": "enum",
                "subtype": None,
                "class_name": param_value.__class__.__name__
            }
        case list():
            subtype = None
            cls = None
            if param_value and isinstance(param_value[0], Enum):
                subtype = "enum"
                cls = param_value[0].__class__.__name__
                wrapped_list = [v.value for v in param_value]
            else:
                wrapped_list = param_value

            return {
                "value": wrapped_list,
                "type": "list",
                "subtype": subtype,
                "class_name": cls
            }
        case dict():
            return {"value": param_value, "type": "dict", "subtype": None, "class_name": None}
        case _:
            raise TypeError(f"Unsupported type {type(param_value)} for {param_value}")
