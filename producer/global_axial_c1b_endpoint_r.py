"""C1b endpoint-safe R evaluator (producer lineage only)."""
from flint import arb
from producer import global_axial_c0_producer as base


class REndpointDomainGuard(RuntimeError):
    pass


def _R_point(x):
    if x == 0:
        return arb(1)
    if x == 1:
        return arb.pi() / 2
    y = x.sqrt()
    if not y.upper() <= 1:
        raise REndpointDomainGuard("R_ENDPOINT_DOMAIN_GUARD")
    return y.asin() / y


def _R_endpoint_safe(u, stats):
    lo = max(arb(0), u.lower())
    hi = min(arb(1), u.upper())
    if hi < lo:
        raise REndpointDomainGuard("R_ENDPOINT_EMPTY")
    rlo = _R_point(lo)
    rhi = _R_point(hi)
    stats["endpoint_safe"] = stats.get("endpoint_safe", 0) + 1
    return base._box(rlo.lower(), rhi.upper())
