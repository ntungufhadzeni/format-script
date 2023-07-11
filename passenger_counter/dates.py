
def add_week(name):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    weekends = ['Sunday', 'Saturday']
    if name in weekends:
        return 'Weekend'
    elif name in weekdays:
        return 'Weekday'
