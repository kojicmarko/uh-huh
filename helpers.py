import datetime


def get_sec(time):
    """Get seconds from time string."""
    h, m, s = [int(t) for t in time.split(':')]
    return datetime.timedelta(hours=h, minutes=m, seconds=s).total_seconds()


def get_time_str(seconds):
    """Get time string from seconds"""
    return str(datetime.timedelta(seconds=seconds)).split('.')[0]


def lst_to_csv_str(list):
    """Convert a list to CSV string"""
    s = ''
    for data in list:
        if not data:
            s += ','
        else:
            s += f'{str(data).strip()},'
    return f'{s}\n'
