import logging
import pyRAPL

_state = 0
_prev = None
_totals = []

def _restart():
    m = pyRAPL.Measurement("prometheus")
    m.begin()
    return m

def _bootstrap_sockets():
    probe = pyRAPL.Measurement("probe")
    probe.begin()
    probe.end()
    return len(probe.result.pkg)

def metrics():
    global _state, _prev, _totals

    if _state == -1:
        return []

    if _state == 0:
        if pyRAPL is None:
            _state = -1
            return []
        try:
            pyRAPL.setup()
            n_sock = _bootstrap_sockets()
            _totals = [0.0] * n_sock
            out = [
                ("rapl_energy_joules_total", {"socket": i}, 0.0)
                for i in range(n_sock)
            ]
            _prev = _restart()
            _state = 1
            logging.info(f"RAPL collector enabled ({n_sock} sockets)")
            return out
        except Exception as e:
            logging.warning(f"RAPL disabled: {e}")
            _state = -1
            return []

    _prev.end()
    for i, delta in enumerate(_prev.result.pkg):
        _totals[i] += float(delta)
    out = [
        ("rapl_energy_joules_total", {"socket": i}, t)
        for i, t in enumerate(_totals)
    ]
    _prev = _restart()
    return out
