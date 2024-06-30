from .core import IntersectionTrafficFlow as IntersectionTrafficFlowClass

def IntersectionTrafficFlow(*args, **kwargs):
    return IntersectionTrafficFlowClass(*args, **kwargs)

__all__ = ['IntersectionTrafficFlow']