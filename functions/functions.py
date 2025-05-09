def beautify_ubi(number):
    ubi = str(number)
    if len(ubi) < 3:
        nulls = 3 - len(ubi)
        for i in range(nulls):
            ubi = '0' + ubi
    return ubi


def check_bool(value):
    if value:
        return 'Да'
    else:
        return 'Нет'
