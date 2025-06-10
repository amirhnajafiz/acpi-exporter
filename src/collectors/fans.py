import logging, psutil

def metrics():
    out = []
    try:
        for dev, entries in psutil.sensors_fans().items():
            for idx, e in enumerate(entries):
                fan_lbl = (e.label or f"{dev}_{idx}").replace(" ", "_").lower()
                out.append(
                    ("fan_speed_rpm",  # one metric for all fans
                     {"device": dev, "fan": fan_lbl},
                     float(e.current))
                )
    except AttributeError:
        pass
    return out
