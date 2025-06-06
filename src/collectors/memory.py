import psutil

def metrics():
    m = psutil.virtual_memory()
    return [
        ("host_mem_total_bytes",     {}, m.total),
        ("host_mem_used_bytes",      {}, m.used),
        ("host_mem_free_bytes",      {}, m.free),
        ("host_mem_available_bytes", {}, m.available),
        ("host_mem_cached_bytes",    {}, m.cached),
    ]
