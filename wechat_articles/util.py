from datetime import datetime


def within_one_week(create_timestamp):
    latest_monday = datetime(2020, 9, 7, 0, 0)
    create_time = datetime.fromtimestamp(create_timestamp)

    return create_time > latest_monday