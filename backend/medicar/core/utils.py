import datetime
from django.conf import settings


def get_data_hoje(past_days):
    return datetime.datetime.now() - datetime.timedelta(days=past_days)


def str_to_date(date_string):
    return datetime.datetime.strptime(date_string, settings.DATE_INPUT_FORMATS[0])
