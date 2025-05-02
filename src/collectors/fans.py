import psutil

def metrics() -> dict[str, float]:
    out = {}
    try:
        fans = psutil.sensors_fans()
    except AttributeError:
        return {}
    for dev, entries in fans.items():
        for idx, e in enumerate(entries):
            label = (e.label or f"{dev}_{idx}").replace(" ", "_").lower()
            out[f"{label}_rpm"] = float(e.current)
    return out

