from datetime import datetime


def format_time_to_hours_and_minutes(time):
    return datetime.fromisoformat(time + '.000+00:00').strftime('%H:%M')


def format_time_to_day_and_month(time):
    return datetime.fromisoformat(time + '.000+00:00').strftime('%d %B')
