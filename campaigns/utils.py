from datetime import date

from sos_brazil.exceptions import BadEndDateException, BadStartDateException


def check_dates(start_date, end_date):
    if start_date < date.today():
        raise BadStartDateException()

    elif start_date > end_date:
        raise BadEndDateException()
