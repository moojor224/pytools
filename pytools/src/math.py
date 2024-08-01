def roundf(val: float, base: float) -> float:
    """rounds val to the nearest multiple of base"""
    return round(val / base) * base


def clamp(val, minval, maxval):
    return max(min(val, maxval), minval)


def map(val, inmin, inmax, outmin, outmax):
    return (val - inmin) * (outmax - outmin) / (inmax - inmin) + outmin
