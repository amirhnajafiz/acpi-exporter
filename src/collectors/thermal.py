import psutil

def metrics() -> dict[str, float]:
    out = {}
    temps = psutil.sensors_temperatures(fahrenheit=False)
    for dev, entries in temps.items():
        for e in entries:
            label = (e.label or "temp").replace(" ", "_").lower()
            out[f"{dev}_{label}"] = float(e.current)
    return out
