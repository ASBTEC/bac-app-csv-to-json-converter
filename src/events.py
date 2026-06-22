import datetime
from typing import Optional

CATEGORY_MAP: dict[str, str] = {
    "General": "general",
    "bioBAC": "bioBAC",
    "businessBAC": "businessBAC",
    "expoBAC": "expoBAC",
    "viveBAC": "viveBAC",
}

LANGUAGE_MAP: dict[str, str] = {
    "Español": "spanish",
    "Inglés": "english",
}


def _build_datetime(day_val, time_val) -> Optional[str]:
    if day_val is None or time_val is None:
        return None
    if isinstance(day_val, str):
        try:
            date = datetime.datetime.strptime(day_val, "%Y/%m/%d").date()
        except ValueError:
            return None
    elif isinstance(day_val, datetime.datetime):
        date = day_val.date()
    elif isinstance(day_val, datetime.date):
        date = day_val
    else:
        return None
    if not isinstance(time_val, datetime.time):
        return None
    return datetime.datetime.combine(date, time_val).isoformat()


def _split_csv(value) -> list[str]:
    if not value:
        return []
    return [v.strip() for v in str(value).split(",") if v.strip()]


def transform_event(row: dict) -> dict:
    event: dict = {
        "id": row["ID"],
        "title": row.get("Título del evento"),
        "description": row.get("Descripción evento"),
        "category": CATEGORY_MAP.get(row.get("Categoría"), row.get("Categoría")),
        "activity_type": row.get("Tipo de actividad"),
        "start_time": _build_datetime(row.get("Día"), row.get("Hora inicio")),
        "end_time": _build_datetime(row.get("Día"), row.get("Hora fin")),
        "local_location": row.get("Ubicación"),
        "language": LANGUAGE_MAP.get(row.get("Idioma"), row.get("Idioma")),
    }

    exhibitor_ids = _split_csv(row.get("ID exhibitor"))
    if exhibitor_ids:
        event["exhibitor_ids"] = exhibitor_ids

    biotech_colors = [c for c in _split_csv(row.get("Color biotech")) if c.lower() != "no aplica"]
    if biotech_colors:
        event["biotech_color"] = biotech_colors

    location = row.get("Enlace Maps")
    if location and location.strip() != "Universitat Autònoma de Barcelona":
        event["location"] = location

    return event
