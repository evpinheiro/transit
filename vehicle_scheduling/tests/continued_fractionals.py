import math
"""
http://sites.math.rutgers.edu/~sk1233/courses/ANT-F14/lec2.pdf

"""


def next(value, next_a, previous_value):
    return value * next_a + previous_value


def sequence(list_sequence, n_plus_one, _value0, _value1):
    result = list()
    _value0 = _value0
    _value1 = _value1
    result.append(_value0)
    result.append(_value1)
    for i in range(2, n_plus_one):
        next_value = next(_value1, list_sequence[i], + _value0)
        result.append(next_value)
        _value1 = next_value
        _value0 = _value1
    return result


def p_sequence(list_sequence, n_plus_one):
    q0 = list_sequence[0]
    q1 = q0 * list_sequence[1] + 1
    return sequence(list_sequence, n_plus_one, q0, q1)


def q_sequence(list_sequence, n_plus_one):
    q0 = 1
    q1 = list_sequence[1]
    return sequence(list_sequence, n_plus_one, q0, q1)


def continued_fraction_sequence(value, _n):
    vector = []
    next_value = value
    max_int_lower = math.floor(next_value)
    _i = 0
    while _i < _n and max_int_lower >= 0:
        vector.append(max_int_lower)
        next_value = 1 / (next_value - max_int_lower)
        max_int_lower = math.floor(next_value) \
            if (math.ceil(next_value) - next_value > 1e-6) else math.ceil(next_value)
        _i = _i + 1
    return vector


a_list = continued_fraction_sequence(19/12, 20)
n = 5
qn = q_sequence(a_list, n)
pn = p_sequence(a_list, n)
print(qn)
print(pn)
for i in range(n):
    if qn[i] <= 5 and pn[i] > 0:
        print(i, pn[i]/qn[i])

