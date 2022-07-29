from datetime import date

from sos_brazil.exceptions import CampaignDateException
from sos_brazil.settings import DATE_INPUT_FORMATS as dt_format


def check_dates(start_date: date, end_date: date):
    if start_date > end_date:
        raise CampaignDateException(
            messages={
                "start_date": start_date.strftime(dt_format[0]),
                "end_date": end_date.strftime(dt_format[0]),
            },
        )
