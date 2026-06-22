EXHIBITOR_TYPE_MAP: dict[str, str] = {
    "Speaker": "speaker",
    "Entidades Colaboradoras": "business",
    "Comité Científico": "speaker",
}

SPONSOR_TIER_MAP: dict[str, str] = {
    "Platino": "platinum",
    "Plata": "silver",
    "Bronce": "bronze",
}


def transform_exhibitor(row: dict) -> dict:
    exhibitor: dict = {
        "id": row["ID exhibitor"],
        "exhibitor_type": EXHIBITOR_TYPE_MAP.get(row.get("Tipo expositor"), row.get("Tipo expositor")),
        "name": row.get("Nombre"),
        "photo": row.get("Foto"),
        "description": row.get("Descripción") or "",
    }

    tier = SPONSOR_TIER_MAP.get(row.get("Sponsor tier", ""))
    if tier:
        exhibitor["sponsor_tier"] = tier

    return exhibitor
