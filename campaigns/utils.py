from datetime import date

from sos_brazil.exceptions import CampaignDateException
from sos_brazil.settings import DATE_INPUT_FORMATS as dt_format


def check_dates(start_date: date, end_date: date, instance):
    if start_date and not end_date:
        end_date = instance.end_date

    elif end_date and not start_date:
        start_date = instance.start_date

    if start_date > end_date:
        raise CampaignDateException(
            messages={
                "start_date": start_date.strftime(dt_format[0]),
                "end_date": end_date.strftime(dt_format[0]),
            },
        )
