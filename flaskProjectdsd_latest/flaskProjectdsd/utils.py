def format_time(time):
    hour, minute = map(int, time.split(':'))
    return f'{hour:02}:{minute:02}'