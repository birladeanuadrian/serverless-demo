import re
from dataclasses import asdict, dataclass, fields

from app.exceptions import InvalidDataException


@dataclass
class AbstractModel:
    def as_json(self):
        data = asdict(self)
        if data.get("_id", False) is None:
            del data["_id"]
        elif data.get("_id"):
            data["_id"] = str(data["_id"])
        return data

    @classmethod
    def build(cls, data: dict):
        if not data:
            raise InvalidDataException("Data is missing")

        try:
            return cls(**data)
        except TypeError as exc:
            match = re.search(r"'(.*?)'", str(exc))

            if match:
                field = match.group(1)
                raise InvalidDataException(f"Invalid field identified.", field)
            else:
                raise InvalidDataException("Invalid data sent")
