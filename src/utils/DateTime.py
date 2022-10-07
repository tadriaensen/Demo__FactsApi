from datetime import datetime, time
import datetime as dt
import dateutil.parser
import math


def create_date_object(year: int, month: int, day: int) -> datetime:
    return datetime(year, month, day)


def create_time_object(hour: int, minute: int, seconds: int) -> time:
    return time(hour=hour, minute=minute, second=seconds)


def diff(timestamp1: datetime = None, timestamp2: datetime = None):
    return_value = {'timestamp1': format_timestamp(timestamp=timestamp1, output_format='%Y-%m-%d %H:%M:%S'), 'timestamp2': format_timestamp(timestamp=timestamp2, output_format='%Y-%m-%d %H:%M:%S')}
    if (timestamp1 - timestamp2).total_seconds() >= 0:
        return_value['timestamp1_earlier_than_timestamp2'] = False
    else:
        return_value['timestamp1_earlier_than_timestamp2'] = True

    return_value['difference'] = {}
    if return_value['timestamp1_earlier_than_timestamp2']:
        var_diff = (timestamp2 - timestamp1).total_seconds()
    else:
        var_diff = (timestamp2 - timestamp1).total_seconds()

    return_value['difference']['days'] = math.floor(var_diff // 86400)
    if return_value['difference']['days'] == 0:
        return_value['difference_string'] = ''
    elif return_value['difference']['days'] == 1:
        return_value['difference_string'] = '{} day'.format(return_value['difference']['days'])
    else:
        return_value['difference_string'] = '{} days'.format(return_value['difference']['days'])

    var_diff = var_diff % 86400
    return_value['difference']['hours'] = math.floor(var_diff // 3600)
    if return_value['difference']['hours'] == 0:
        if not return_value['difference_string'] == '':
            return_value['difference_string'] = '{}, {} hours'.format(return_value['difference_string'], return_value['difference']['hours'])
    elif return_value['difference']['hours'] == 1:
        if return_value['difference_string'] == '':
            return_value['difference_string'] = '{} hour'.format(return_value['difference']['hours'])
        else:
            return_value['difference_string'] = '{}, {} hour'.format(return_value['difference_string'], return_value['difference']['hours'])
    else:
        if return_value['difference_string'] == '':
            return_value['difference_string'] = '{} hours'.format(return_value['difference']['hours'])
        else:
            return_value['difference_string'] = '{}, {} hours'.format(return_value['difference_string'], return_value['difference']['hours'])

    var_diff = var_diff % 3600
    return_value['difference']['minutes'] = math.floor(var_diff // 60)
    if return_value['difference']['minutes'] == 0:
        if not return_value['difference_string'] == '':
            return_value['difference_string'] = '{}, {} minutes'.format(return_value['difference_string'], return_value['difference']['minutes'])
    elif return_value['difference']['minutes'] == 1:
        if return_value['difference_string'] == '':
            return_value['difference_string'] = '{} minute'.format(return_value['difference']['minutes'])
        else:
            return_value['difference_string'] = '{}, {} minute'.format(return_value['difference_string'], return_value['difference']['minutes'])
    else:
        if return_value['difference_string'] == '':
            return_value['difference_string'] = '{} minutes'.format(return_value['difference']['minutes'])
        else:
            return_value['difference_string'] = '{}, {} minutes'.format(return_value['difference_string'], return_value['difference']['minutes'])

    var_diff = var_diff % 60
    return_value['difference']['seconds'] = math.floor(var_diff)
    if return_value['difference']['seconds'] == 0:
        if return_value['difference_string'] == '':
            return_value['difference_string'] = '{} seconds'.format(return_value['difference']['seconds'])
        else:
            return_value['difference_string'] = '{}, {} seconds'.format(return_value['difference_string'], return_value['difference']['seconds'])
    elif return_value['difference']['seconds'] == 1:
        if return_value['difference_string'] == '':
            return_value['difference_string'] = '{} second'.format(return_value['difference']['seconds'])
        else:
            return_value['difference_string'] = '{}, {} second'.format(return_value['difference_string'], return_value['difference']['seconds'])
    else:
        if return_value['difference_string'] == '':
            return_value['difference_string'] = '{} seconds'.format(return_value['difference']['seconds'])
        else:
            return_value['difference_string'] = '{}, {} seconds'.format(return_value['difference_string'], return_value['difference']['seconds'])

    return return_value


def format_timestamp(timestamp: datetime, output_format='%Y-%m-%d %H:%M:%S') -> str:
    return timestamp.strftime(output_format)


def get_day_time_periods(interval_in_minutes: int) -> dict:
    return_value = {'time_periods': []}

    if type(interval_in_minutes) == int and interval_in_minutes > 0:
        hours = 0
        minutes = 0
        generated_time_periods = []
        while hours < 24:
            tmp_object = {'hour': hours, 'minute': minutes, 'string_value': '{}:{}'.format(str(hours).zfill(2), str(minutes).zfill(2))}

            generated_time_periods.append(tmp_object)

            minutes = minutes + interval_in_minutes
            if minutes > 59:
                hours = hours + int(minutes / 60)
                minutes = int(minutes % 60)

        return_value['time_periods'] = generated_time_periods

    return return_value


def get_date_details(timestamp: datetime):
    return_value = {'date_details': {}}
    return_value['date_details']['date'] = format_timestamp(timestamp=timestamp, output_format='%Y-%m-%d')
    return_value['date_details']['time'] = format_timestamp(timestamp=timestamp, output_format='%H:%M:%S')
    return_value['date_details']['timestamp'] = get_timestamp_formatted_iso(timestamp=timestamp)
    return_value['date_details']['timestamp_with_microseconds'] = get_timestamp_formatted_iso_with_microseconds(timestamp=timestamp)
    return_value['date_details']['quarter'] = get_quarter(timestamp=timestamp)
    return_value['date_details']['date_details'] = {}
    return_value['date_details']['date_details']['year'] = timestamp.year
    return_value['date_details']['date_details']['month'] = get_month(timestamp=timestamp)
    return_value['date_details']['date_details']['day'] = timestamp.day
    return_value['date_details']['date_details']['week_number'] = timestamp.isocalendar().week
    return_value['date_details']['date_details']['weekday'] = get_weekday(timestamp=timestamp)
    return_value['date_details']['time_details'] = {}
    return_value['date_details']['time_details']['hour'] = timestamp.hour
    return_value['date_details']['time_details']['minute'] = timestamp.minute
    return_value['date_details']['time_details']['second'] = timestamp.second
    return_value['date_details']['time_details']['microsecond'] = timestamp.microsecond

    return return_value


def get_first_day_of_the_year(year: int = None, output_format='%Y-%m-%d') -> str:
    if year is None:
        year = int(datetime.now().strftime('%Y'))

    return_value = datetime(year, 1, 1).strftime(output_format)
    return return_value


def get_last_day_of_the_year(year: int = None, output_format='%Y-%m-%d') -> str:
    if year is None:
        year = int(datetime.now().strftime('%Y'))

    return_value = datetime(year, 12, 31).strftime(output_format)
    return return_value


def get_timestamp() -> datetime:
    return datetime.now()


def get_timestamp_formatted_iso(timestamp: datetime = None) -> str:
    if timestamp is None:
        return_value = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        return_value = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    return return_value


def get_timestamp_formatted_iso_with_microseconds(timestamp: datetime = None) -> str:
    if timestamp is None:
        return_value = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    else:
        return_value = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
    return return_value


def get_timestamp_from_iso_string(timestamp_string_iso_format: str) -> datetime:
    return dateutil.parser.parse(timestamp_string_iso_format)


def get_today(output_format: str = '%Y-%m-%d') -> str:
    return datetime.now().strftime(output_format)


def get_weekday_list() -> dict:
    return_value = {'weekdays': []}
    return_value['weekdays'].append({'day_nbr': 1, 'day_name': {'english': 'Monday', 'dutch': 'maandag', 'french': 'Mundi', 'german': 'Montag'}})
    return_value['weekdays'].append({'day_nbr': 2, 'day_name': {'english': 'Tuesday', 'dutch': 'dinsdag', 'french': 'Mardi', 'german': 'Dienstag'}})
    return_value['weekdays'].append({'day_nbr': 3, 'day_name': {'english': 'Wednesday', 'dutch': 'woensdag', 'french': 'Mercredi', 'german': 'Mittwoch'}})
    return_value['weekdays'].append({'day_nbr': 4, 'day_name': {'english': 'Thursday', 'dutch': 'donderdag', 'french': 'Jeudi', 'german': 'Donnerstag'}})
    return_value['weekdays'].append({'day_nbr': 5, 'day_name': {'english': 'Friday', 'dutch': 'vrijdag', 'french': 'Vendredi', 'german': 'Freitag'}})
    return_value['weekdays'].append({'day_nbr': 6, 'day_name': {'english': 'Saturday', 'dutch': 'zaterdag', 'french': 'Samedi', 'german': 'Samstag'}})
    return_value['weekdays'].append({'day_nbr': 7, 'day_name': {'english': 'Sunday', 'dutch': 'zondag', 'french': 'Dimanche', 'german': 'Sonntag'}})
    return return_value


def get_weekday(timestamp: datetime = None) -> dict:
    if timestamp is None:
        timestamp = datetime.now()
    weekday_list = get_weekday_list()['weekdays']
    return weekday_list[timestamp.weekday()]


def get_month_list() -> dict:
    return_value = {'months': []}
    return_value['months'].append({'month_nbr': 1, 'month_name': {'english': 'January', 'dutch': 'januari', 'french': 'janvier', 'german': 'Januar'}})
    return_value['months'].append({'month_nbr': 2, 'month_name': {'english': 'February', 'dutch': 'februari', 'french': 'février', 'german': 'Februar'}})
    return_value['months'].append({'month_nbr': 3, 'month_name': {'english': 'March', 'dutch': 'maart', 'french': 'Mars', 'german': 'März'}})
    return_value['months'].append({'month_nbr': 4, 'month_name': {'english': 'April', 'dutch': 'april', 'french': 'Avril', 'german': 'April'}})
    return_value['months'].append({'month_nbr': 5, 'month_name': {'english': 'May', 'dutch': 'mei', 'french': 'Mai', 'german': 'Mai'}})
    return_value['months'].append({'month_nbr': 6, 'month_name': {'english': 'June', 'dutch': 'juni', 'french': 'Juin', 'german': 'Juni'}})
    return_value['months'].append({'month_nbr': 7, 'month_name': {'english': 'July', 'dutch': 'juli', 'french': 'Juillet', 'german': 'Juli'}})
    return_value['months'].append({'month_nbr': 8, 'month_name': {'english': 'August', 'dutch': 'augustus', 'french': 'Août', 'german': 'August'}})
    return_value['months'].append({'month_nbr': 9, 'month_name': {'english': 'September', 'dutch': 'september', 'french': 'Septembre', 'german': 'September'}})
    return_value['months'].append({'month_nbr': 10, 'month_name': {'english': 'October', 'dutch': 'oktober', 'french': 'Octobre', 'german': 'Oktober'}})
    return_value['months'].append({'month_nbr': 11, 'month_name': {'english': 'November', 'dutch': 'november', 'french': 'Novembre', 'german': 'November'}})
    return_value['months'].append({'month_nbr': 12, 'month_name': {'english': 'December', 'dutch': 'december', 'french': 'Décembre', 'german': 'Dezember'}})

    return return_value


def get_month(timestamp: datetime = None) -> dict:
    if timestamp is None:
        timestamp = datetime.now()
    month_list = get_month_list()['months']
    return month_list[timestamp.month - 1]


def get_quarter_list() -> dict:
    return_value = {'quarters': []}
    return_value['quarters'].append({'quarter_nbr': 1, 'quarter_name': 'Q1'})
    return_value['quarters'].append({'quarter_nbr': 2, 'quarter_name': 'Q2'})
    return_value['quarters'].append({'quarter_nbr': 3, 'quarter_name': 'Q3'})
    return_value['quarters'].append({'quarter_nbr': 4, 'quarter_name': 'Q4'})
    return return_value


def get_quarter(timestamp: datetime = None) -> dict:

    if timestamp is None:
        timestamp = datetime.now()
    month_nbr = timestamp.month

    quarter_list = get_quarter_list()['quarters']
    if month_nbr == 1 or month_nbr == 2 or month_nbr == 3:
        return_value = quarter_list[0]
    elif month_nbr == 4 or month_nbr == 5 or month_nbr == 6:
        return_value = quarter_list[1]
    elif month_nbr == 7 or month_nbr == 8 or month_nbr == 9:
        return_value = quarter_list[2]
    elif month_nbr == 10 or month_nbr == 11 or month_nbr == 12:
        return_value = quarter_list[3]
    else:
        return_value = {}

    return return_value


def get_year(timestamp: datetime = None) -> int:
    if timestamp is None:
        return_value = datetime.now().strftime('%Y')
    else:
        return_value = timestamp.strftime('%Y')
    return_value = int(return_value)
    return return_value


def seconds2days_hours_minutes_seconds(seconds_to_convert: int) -> dict:
    converted = {'total_seconds': seconds_to_convert, 'split': {}}
    converted['split']['days'] = 0
    converted['split']['hours'] = 0
    converted['split']['minutes'] = 0
    converted['split']['seconds'] = 0

    seconds = seconds_to_convert
    converted['split']['days'] = math.floor(seconds // 86400)
    if converted['split']['days'] == 0:
        converted['split_string'] = ''
    elif converted['split']['days'] == 1:
        converted['split_string'] = '{} day'.format(converted['split']['days'])
    else:
        converted['split_string'] = '{} days'.format(converted['split']['days'])

    seconds = seconds % 86400
    converted['split']['hours'] = math.floor(seconds // 3600)
    if converted['split']['hours'] == 0:
        if not converted['split_string'] == '':
            converted['split_string'] = '{}, {} hours'.format(converted['split_string'], converted['split']['hours'])
    elif converted['split']['hours'] == 1:
        if converted['split_string'] == '':
            converted['split_string'] = '{} hour'.format(converted['split']['hours'])
        else:
            converted['split_string'] = '{}, {} hour'.format(converted['split_string'], converted['split']['hours'])
    else:
        if converted['split_string'] == '':
            converted['split_string'] = '{} hours'.format(converted['split']['hours'])
        else:
            converted['split_string'] = '{}, {} hours'.format(converted['split_string'], converted['split']['hours'])

    seconds = seconds % 3600
    converted['split']['minutes'] = math.floor(seconds // 60)
    if converted['split']['minutes'] == 0:
        if not converted['split_string'] == '':
            converted['split_string'] = '{}, {} minutes'.format(converted['split_string'], converted['split']['minutes'])
    elif converted['split']['minutes'] == 1:
        if converted['split_string'] == '':
            converted['split_string'] = '{} minute'.format(converted['split']['minutes'])
        else:
            converted['split_string'] = '{}, {} minute'.format(converted['split_string'], converted['split']['minutes'])
    else:
        if converted['split_string'] == '':
            converted['split_string'] = '{} minutes'.format(converted['split']['minutes'])
        else:
            converted['split_string'] = '{}, {} minutes'.format(converted['split_string'], converted['split']['minutes'])

    seconds = seconds % 60
    converted['split']['seconds'] = math.floor(seconds)
    if converted['split']['seconds'] == 0:
        if converted['split_string'] == '':
            converted['split_string'] = '{} seconds'.format(converted['split']['seconds'])
        else:
            converted['split_string'] = '{}, {} seconds'.format(converted['split_string'], converted['split']['seconds'])
    elif converted['split']['seconds'] == 1:
        if converted['split_string'] == '':
            converted['split_string'] = '{} second'.format(converted['split']['seconds'])
        else:
            converted['split_string'] = '{}, {} second'.format(converted['split_string'], converted['split']['seconds'])
    else:
        if converted['split_string'] == '':
            converted['split_string'] = '{} seconds'.format(converted['split']['seconds'])
        else:
            converted['split_string'] = '{}, {} seconds'.format(converted['split_string'], converted['split']['seconds'])

    return converted


def timestamp_add_days(timestamp: datetime, days_to_add: int) -> datetime:
    return timestamp + dt.timedelta(days=days_to_add)


def timestamp_subtract_days(timestamp: datetime, days_to_subtract: int) -> datetime:
    return timestamp - dt.timedelta(days=days_to_subtract)
