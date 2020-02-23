from copy import deepcopy
from typing import Dict
from jikanpy_ext.extension import Extension, Context

def flatten_dict(d: Dict):
    """Recursively flatten dictionaries, ordered by keys in ascending order"""
    s = ""
    for k in sorted(d.keys()):
        if d[k] is not None:
            if isinstance(d[k], dict):
                s += f"{k}|{flatten_dict(d[k])}|"
            else:
                s += f"{k}|{d[k]}|"
    return s


def stringify(ctx: Context):
    """Convert a request to a unique string representation"""
    return f"{str(ctx.request_name)}|{flatten_dict(deepcopy(ctx.jikanpy_kwargs))}"
