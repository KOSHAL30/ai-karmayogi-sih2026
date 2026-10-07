import types
from typing import Optional

def _to_obj(doc: dict) -> types.SimpleNamespace:
    if not doc:
        return None
    d = dict(doc)
    if "_id" in d:
        d["id"] = str(d.pop("_id"))
    return types.SimpleNamespace(**d)

doc = {
    "_id": "11111111",
    "department_code": "DEPT-DOPT",
    "department_name": "DoPT"
}
dept = _to_obj(doc)
print(dept)
print(getattr(dept, "name", "None!"))
try:
    print(dept.name)
except Exception as e:
    print(repr(e))
