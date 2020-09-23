import datetime


def get_data_hoje(past_days):
    return datetime.datetime.now() - datetime.timedelta(days=past_days)