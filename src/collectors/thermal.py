import psutil

def metrics() -> dict[str, float]:
    out = {}
    try:
        temps = psutil.sensors_temperatures(fahrenheit=False)
        for dev, entries in temps.items():
            for e in entries:
                label = (e.label or "temp").replace(" ", "_").lower()
                out[f"{dev}_{label}"] = float(e.current)
    except AttributeError:
        # handle platforms where sensors_temperatures is not supported
        print("Temperature sensors are not supported on this platform.")
    return out
