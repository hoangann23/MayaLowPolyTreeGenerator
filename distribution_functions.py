import math
import random

def sin(**kwargs):
    total =  kwargs.get('total', None)
    concentration_min = kwargs.get('concentration_min', None)
    concentration_max = kwargs.get('concentration_max', None)
    x = kwargs.get('x', None)
    # concentration_min and concentration_max should be a percentage value
    # within concentration_min * total and concentration_max * toatal -> output sin value
    # else output 0
    if x >= concentration_min * total and x <= concentration_max * total:
        def normalize(val, min_value, max_value, target_min, target_max):
            return target_min + (((val - min_value) * (target_max - target_min)) / (max_value - min_value))
        # convert x to corresponding radian value: [concentration_min*total, concentration_max*total] -> [0, pi]
        out = math.sin(normalize(x, concentration_min*total, concentration_max*total, 0, math.pi)) 
        roundToInt = kwargs.get("roundToInt", False)
        if roundToInt == True:
            return round(out * kwargs.get('maxValue', None)) 
        else:
            return out
    return 0

def randInt(**kwargs):
    roundToInt = kwargs.get("roundToInt", False)
    if roundToInt == True:
        return random.randint(0, kwargs.get('maxValue', 0))
    return random.uniform(0, kwargs.get("maxValue", 0))

def linear(**kwargs):
    initial_value = kwargs.get("initial_value", None) # value at concentration_min
    end_value = kwargs.get("end_value", None) # value at concentration_max
    concentration_min = kwargs.get('concentration_min', None)
    concentration_max = kwargs.get('concentration_max', None)
    total = kwargs.get('total', None)

    slope = (end_value - initial_value) / ((concentration_max*total) - (concentration_min*total))
    intersect = end_value - (slope * (concentration_max*total))
    x = kwargs.get("x", 0)
    out = slope * x + intersect
    roundToInt = kwargs.get("roundToInt", False)
    if roundToInt == True:
        return round(out) 
    else:
        return out
