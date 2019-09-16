import string


def minutes(hhmm: string):
    h, m = hhmm.split(':')
    return int(h)*60+int(m)


def hour_minute(mm: int):
    h = int(mm/60)
    return f'{format_number(h)}:{format_number(mm-60*h)}'


def format_number(time):
    return  ("0" if time < 10 else "") + str(time)