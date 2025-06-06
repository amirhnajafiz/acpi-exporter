import logging, psutil

def metrics():
    out = []
    try:
        for dev, entries in psutil.sensors_temperatures(fahrenheit=False).items():
            for e in entries:
                label = (e.label or "temp").strip()
                if dev == "coretemp" and label.lower().startswith("core"):
                    try:
                        core_id = int("".join(filter(str.isdigit, label)))
                    except ValueError:
                        core_id = label
                    out.append(("cpu_core_temp_celsius", {"core_number": core_id}, float(e.current)))
                else:
                    mname = f"{dev}_{label.replace(' ', '_').lower()}_celsius"
                    out.append((mname, {}, float(e.current)))
    except AttributeError:
        # handle platforms where sensors_temperatures is not supported
        logging.error("temperature sensors are not supported on this platform.")
    return out
