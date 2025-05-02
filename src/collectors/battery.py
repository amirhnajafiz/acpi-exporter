import psutil

def metrics() -> dict[str, float]:
    bat = psutil.sensors_battery()
    if bat is None:
        return {}
    return {
        "battery_pct": float(bat.percent),
        "battery_secs_left": float(bat.secsleft),
    }

