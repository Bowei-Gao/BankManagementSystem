from datetime import datetime

import arrow


def get_quarter(number):
    """
    number 传入季度之间的月份就可以了
    :param number:
    :return:
    """
    if number == 1:
        data = 2
    elif number == 2:
        data = 5
    elif number == 3:
        data = 8
    elif number == 4:
        data = 11
    quarter = datetime(datetime.now().year, data, data)
    quarter = arrow.get(quarter).span('quarter')
    start = quarter[0].strftime('%Y-%m-%d %H:%M:%S')
    end = quarter[1].strftime('%Y-%m-%d %H:%M:%S')
    return start, end


def get_month(number):
    """
    number 季度
    :param number:
    :return:
    """
    if number > 12:
        raise Exception(ValueError)
    quarter = datetime(datetime.now().year, number, number)
    quarter = arrow.get(quarter).span('month')
    start = quarter[0].strftime('%Y-%m-%d %H:%M:%S')
    end = quarter[1].strftime('%Y-%m-%d %H:%M:%S')
    return start, end


def get_year(number):
    """
    number 年
    :param number:
    :return:
    """
    if number == 0:
        quarter = datetime(datetime.now().year, 1, 1)

    else:
        quarter = datetime(datetime.now().year - number, 1, 1)
        year = datetime(datetime.now().year-number, 1, 1)

    quarter = arrow.get(quarter).span('year')
    start = quarter[0].strftime('%Y-%m-%d %H:%M:%S')
    end = quarter[1].strftime('%Y-%m-%d %H:%M:%S')
    return start, end, str(year.year)+'年'
