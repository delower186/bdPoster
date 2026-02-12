from datetime import datetime
# ------------------------------
# Helpers
# ------------------------------

DATE_COLUMNS = {"created_at", "updated_at"}

def format_keys(data):
    return ",".join([f"`{k}`" for k in data.keys()])

def format_place_holders(data):
    return ",".join(["%s"] * len(data))

def format_values(data):
    vals = []
    for k, v in data.items():
        if k in DATE_COLUMNS and v:
            # Convert ISO8601 to YYYY-MM-DD
            if isinstance(v, str) and "T" in v:
                v = v.split("T")[0]
            elif isinstance(v, datetime):
                v = v.date().isoformat()
        vals.append(v)
    return vals

