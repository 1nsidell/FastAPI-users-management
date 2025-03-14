from datetime import datetime, timezone


def to_utc_converter() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)
